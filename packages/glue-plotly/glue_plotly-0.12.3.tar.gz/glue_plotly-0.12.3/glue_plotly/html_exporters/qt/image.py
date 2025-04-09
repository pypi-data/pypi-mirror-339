from __future__ import absolute_import, division, print_function

from qtpy import compat
from qtpy.QtWidgets import QDialog

from glue.config import viewer_tool
from glue_qt.utils import messagebox_on_error
from glue_qt.utils.threading import Worker
from glue_qt.viewers.common.tool import Tool

from glue_plotly import PLOTLY_ERROR_MESSAGE, PLOTLY_LOGO
from glue_plotly.common import data_count, layers_to_export
from glue_plotly.common.image import axes_data_from_mpl, layers_by_type, layout_config, traces
from glue_plotly import export_dialog
from glue_plotly.html_exporters.hover_utils import hover_data_collection_for_viewer
from glue_plotly.html_exporters.qt.save_hover import SaveHoverDialog

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots

DEFAULT_FONT = 'Arial, sans-serif'


@viewer_tool
class PlotlyImage2DExport(Tool):
    icon = PLOTLY_LOGO
    tool_id = 'save:plotlyimage2d'
    action_text = 'Save Plotly HTML page'
    tool_tip = 'Save Plotly HTML page'

    @messagebox_on_error(PLOTLY_ERROR_MESSAGE)
    def _export_to_plotly(self, filename, checked_dictionary, config):

        layers = layers_to_export(self.viewer)
        add_data_label = data_count(layers) > 1

        secondary_x = 'xaxis2' in config
        secondary_y = 'yaxis2' in config

        if secondary_x or secondary_y:
            fig = make_subplots(specs=[[{"secondary_y": True}]], horizontal_spacing=0, vertical_spacing=0)
            fig.update_layout(**config)
        else:
            layout = go.Layout(**config)
            fig = go.Figure(layout=layout)

        traces_to_add = traces(self.viewer, secondary_x=secondary_x, secondary_y=secondary_y,
                               hover_selections=checked_dictionary, add_data_label=add_data_label)
        for trace in traces_to_add:
            fig.add_trace(trace)

        plot(fig, include_mathjax='cdn', filename=filename, auto_open=False)

    def activate(self):

        layers = layers_by_type(self.viewer)
        scatter_layers = layers["scatter"]

        if len(scatter_layers) > 0:
            dc_hover = hover_data_collection_for_viewer(
                self.viewer,
                layer_condition=lambda layer: layer.state.visible and layer.enabled and layer in scatter_layers
            )

            dialog = SaveHoverDialog(data_collection=dc_hover)
            result = dialog.exec_()
            if result == QDialog.Rejected:
                return
            checked_dictionary = dialog.checked_dictionary
        else:
            checked_dictionary = None

        filename, _ = compat.getsavefilename(parent=self.viewer, basedir="plot.html")
        if not filename:
            return

        # It would be better to create the layout config in `_export_to_plotly`.
        # But we get some of our axis font sizes from matplotlib, some of which seems to cause problems
        # when run in a QThread. So for now, we get the layout config here.
        config = layout_config(self.viewer)
        ax = axes_data_from_mpl(self.viewer)
        config.update(**ax)
        config["showlegend"] = len(layers) > 1

        worker = Worker(self._export_to_plotly, filename, checked_dictionary, config)
        exp_dialog = export_dialog.ExportDialog(parent=self.viewer)
        worker.result.connect(exp_dialog.close)
        worker.error.connect(exp_dialog.close)
        worker.start()
        exp_dialog.exec_()
