"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
from justin_functions import on_transform_changed_drag

if TYPE_CHECKING:
    import napari


class create_registration_viewer(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        print("Running spatial registration widget...")
        super().__init__()
        self.viewer = napari_viewer
        # set up interaction box for moving/scaling fg_img
        self.viewer.layers.selection.active.interactive = False
        self.viewer.overlays.interaction_box.points = self.viewer.layers.selection.active.extent.world
        self.viewer.overlays.interaction_box.show = True
        self.viewer.overlays.interaction_box.show_vertices = True
        self.viewer.overlays.interaction_box.show_handle = True
        self.viewer.overlays.interaction_box.allow_new_selection = False
        self.viewer.overlays.interaction_box.events.transform_drag.connect(on_transform_changed_drag)

        btn = QPushButton("Capture Affine")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        """
        Extract the inverse of the applied affine transformation from napari `registration_viewer`

        Returns
        -------
        affine : np.array
            Affine matrix describing transformation
        scale : tuple
            Scale from affine transformation
        """
        # extract inverse of affine
        cut = Affine(
            rotate=self.viewer.layers.selection.active.affine.inverse.rotate,
            translate=self.viewer.layers.selection.active.affine.translate[::-1],
        )
        affine = cut.affine_matrix
        # extract scale factor from affine object
        scale = (
            self.viewer.layers.selection.active.affine.scale[0],
            self.viewer.layers.selection.active.affine.scale[1],
            1,  # for 3D image
        )
        return affine, scale


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
