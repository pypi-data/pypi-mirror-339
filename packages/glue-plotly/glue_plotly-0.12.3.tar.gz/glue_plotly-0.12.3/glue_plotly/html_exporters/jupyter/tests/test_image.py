import os

from glue.core import Data

from pytest import importorskip

importorskip('glue_jupyter')

from glue_jupyter.bqplot.image import BqplotImageView  # noqa: E402

from numpy import arange, ones  # noqa: E402

from .test_base import BaseTestJupyterExporter  # noqa: E402


class TestImage(BaseTestJupyterExporter):

    viewer_type = BqplotImageView
    tool_id = 'save:bqplot_plotlyimage2d'

    def make_data(self):
        return Data(label='d1', x=arange(24).reshape((2, 3, 4)), y=ones((2, 3, 4)))

    def test_default(self, tmpdir):
        output_path = self.export_figure(tmpdir, 'test_default.html')
        assert os.path.exists(output_path)
