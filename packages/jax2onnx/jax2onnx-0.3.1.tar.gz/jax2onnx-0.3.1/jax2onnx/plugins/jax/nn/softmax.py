from jax import core
from jax.extend.core import Primitive
import jax.nn as nn
from onnx import helper
from typing import TYPE_CHECKING
from jax2onnx.plugin_system import register_primitive, PrimitivePlugin

if TYPE_CHECKING:
    from jax2onnx.converter.converter import Jaxpr2OnnxConverter

# Define a new primitive for softmax
nn.softmax_p = Primitive("nn.softmax")
nn.softmax_p.multiple_results = False  # Correct initialization


@register_primitive(
    jaxpr_primitive=nn.softmax_p.name,
    jax_doc="https://jax.readthedocs.io/en/latest/_autosummary/jax.nn.softmax.html",
    onnx=[
        {
            "component": "Softmax",
            "doc": "https://onnx.ai/onnx/operators/onnx__Softmax.html",
        }
    ],
    since="v0.1.0",
    context="primitives.nn",
    testcases=[
        {
            "testcase": "softmax",
            "callable": lambda x: nn.softmax(x),
            "input_shapes": [(3,)],
        },
        {
            "testcase": "softmax_2d",
            "callable": lambda x: nn.softmax(x, axis=1),
            "input_shapes": [(4, 5)],
        },
        {
            "testcase": "softmax_3d",
            "callable": lambda x: nn.softmax(x, axis=2),
            "input_shapes": [(2, 3, 4)],
        },
    ],
)
class SoftmaxPlugin(PrimitivePlugin):
    """
    Plugin for converting jax.nn.softmax to ONNX.
    """

    @staticmethod
    def abstract_eval(x, axis=-1):
        """Computes the output shape for nn.softmax."""
        return core.ShapedArray(x.shape, x.dtype)

    def to_onnx(self, s: "Jaxpr2OnnxConverter", node_inputs, node_outputs, params):
        """Handles ONNX conversion for nn.softmax."""
        input_var = node_inputs[0]
        output_var = node_outputs[0]

        input_name = s.get_name(input_var)
        output_name = s.get_name(output_var)

        # Retrieve the axis parameter (defaulting to -1 if not provided)
        axis = params.get("axis", -1)

        softmax_node = helper.make_node(
            "Softmax",
            inputs=[input_name],
            outputs=[output_name],
            name=s.get_unique_name("softmax"),
            axis=axis,
        )
        s.add_node(softmax_node)

    @staticmethod
    def _softmax(x, axis=-1):
        """Defines the primitive binding for Softmax."""
        return nn.softmax_p.bind(x, axis=axis)

    @staticmethod
    def get_monkey_patch():
        """Provides patching information for Softmax."""

        def patched_softmax(x, axis=-1):
            return SoftmaxPlugin._softmax(x, axis)

        return patched_softmax

    @staticmethod
    def patch_info():
        """Provides patching information for Softmax."""
        return {
            "patch_targets": [nn],
            "patch_function": lambda _: SoftmaxPlugin.get_monkey_patch(),
            "target_attribute": "softmax",
        }


# Register abstract evaluation function
nn.softmax_p.def_abstract_eval(SoftmaxPlugin.abstract_eval)
