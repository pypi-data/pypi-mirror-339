import os

from glue.core import Data

from pytest import importorskip

importorskip('glue_jupyter')

from glue_jupyter.bqplot.histogram import BqplotHistogramView  # noqa: E402

from .test_base import BaseTestJupyterExporter  # noqa: E402


class TestHistogram(BaseTestJupyterExporter):

    viewer_type = BqplotHistogramView
    tool_id = 'save:bqplot_plotlyhist'

    def make_data(self):
        return Data(x=[40, 41, 37, 63, 78, 35, 19, 100, 35, 86, 84, 99,
                       87, 56, 2, 71, 22, 36, 10, 1, 26, 70, 45, 20, 8],
                    label='d1')

    def test_default(self, tmpdir):
        output_path = self.export_figure(tmpdir, 'test_default.html')
        assert os.path.exists(output_path)
