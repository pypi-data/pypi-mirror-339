

__all__ = (
    "CommonRipple",
    "RectangularRippleBehavior",
    "CircularRippleBehavior",
)

from typing import NoReturn

from kivy.animation import Animation
from kivy.graphics import (
    Color,
    Ellipse,
    StencilPop,
    StencilPush,
    StencilUnUse,
    StencilUse,
)
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.behaviors import ToggleButtonBehavior


class CommonRipple:


    ripple_rad_default = NumericProperty(1)


    ripple_color = ColorProperty(None)

    ripple_alpha = NumericProperty(0.5)


    ripple_scale = NumericProperty(None)


    ripple_duration_in_fast = NumericProperty(0.3)


    ripple_duration_in_slow = NumericProperty(2)


    ripple_duration_out = NumericProperty(0.3)


    ripple_canvas_after = BooleanProperty(True)


    ripple_func_in = StringProperty("out_quad")

    ripple_func_out = StringProperty("out_quad")


    _ripple_rad = NumericProperty()
    _doing_ripple = BooleanProperty(False)
    _finishing_ripple = BooleanProperty(False)
    _fading_out = BooleanProperty(False)
    _no_ripple_effect = BooleanProperty(False)
    _round_rad = ListProperty([0, 0, 0, 0])

    def lay_canvas_instructions(self) -> NoReturn:
        raise NotImplementedError

    def start_ripple(self) -> None:
        if not self._doing_ripple:
            self._doing_ripple = True
            anim = Animation(
                _ripple_rad=self.finish_rad,
                t="linear",
                duration=self.ripple_duration_in_slow,
            )
            anim.bind(on_complete=self.fade_out)
            anim.start(self)

    def finish_ripple(self) -> None:
        if self._doing_ripple and not self._finishing_ripple:
            self._finishing_ripple = True
            self._doing_ripple = False
            Animation.cancel_all(self, "_ripple_rad")
            anim = Animation(
                _ripple_rad=self.finish_rad,
                t=self.ripple_func_in,
                duration=self.ripple_duration_in_fast,
            )
            anim.bind(on_complete=self.fade_out)
            anim.start(self)

    def fade_out(self, *args) -> None:
        rc = self.ripple_color
        if not self._fading_out:
            self._fading_out = True
            Animation.cancel_all(self, "ripple_color")
            anim = Animation(
                ripple_color=[rc[0], rc[1], rc[2], 0.0],
                t=self.ripple_func_out,
                duration=self.ripple_duration_out,
            )
            anim.bind(on_complete=self.anim_complete)
            anim.start(self)

    def anim_complete(self, *args) -> None:
        self._doing_ripple = False
        self._finishing_ripple = False
        self._fading_out = False

        if not self.ripple_canvas_after:
            canvas = self.canvas.before
        else:
            canvas = self.canvas.after

        canvas.remove_group("circular_ripple_behavior")
        canvas.remove_group("rectangular_ripple_behavior")

    def on_touch_down(self, touch):

        super().on_touch_down(touch)
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if not self.disabled:
            self.call_ripple_animation_methods(touch)

            if isinstance(self, ToggleButtonBehavior):
                return super().on_touch_down(touch)
            else:
                return True

    def call_ripple_animation_methods(self, touch) -> None:
        if self._doing_ripple:
            Animation.cancel_all(
                self, "_ripple_rad", "ripple_color", "rect_color"
            )
            self.anim_complete()
        self._ripple_rad = self.ripple_rad_default
        self.ripple_pos = (touch.x, touch.y)

        if self.ripple_color:
            pass
        elif hasattr(self, "theme_cls"):
            self.ripple_color = self.theme_cls.ripple_color
        else:
            # If no theme, set Gray 300.
            self.ripple_color = [
                0.8784313725490196,
                0.8784313725490196,
                0.8784313725490196,
                self.ripple_alpha,
            ]
        self.ripple_color[3] = self.ripple_alpha
        self.lay_canvas_instructions()
        self.finish_rad = max(self.width, self.height) * self.ripple_scale
        self.start_ripple()

    def on_touch_move(self, touch, *args):
        if not self.collide_point(touch.x, touch.y):
            if not self._finishing_ripple and self._doing_ripple:
                self.finish_ripple()
        return super().on_touch_move(touch, *args)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y) and self._doing_ripple:
            self.finish_ripple()
        return super().on_touch_up(touch)

    def _set_ellipse(self, instance, value):
        self.ellipse.size = (self._ripple_rad, self._ripple_rad)

    # Adjust ellipse pos here

    def _set_color(self, instance, value):
        self.col_instruction.a = value[3]


class RectangularRippleBehavior(CommonRipple):


    ripple_scale = NumericProperty(2.75)

    def lay_canvas_instructions(self) -> None:
        if self._no_ripple_effect:
            return

        with self.canvas.after if self.ripple_canvas_after else self.canvas.before:
            if hasattr(self, "radius"):
                if isinstance(self.radius, (float, int)):
                    self.radius = [
                        self.radius,
                    ]
                self._round_rad = self.radius
            StencilPush(group="rectangular_ripple_behavior")
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self._round_rad,
                group="rectangular_ripple_behavior",
            )
            StencilUse(group="rectangular_ripple_behavior")
            self.col_instruction = Color(
                rgba=self.ripple_color, group="rectangular_ripple_behavior"
            )
            self.ellipse = Ellipse(
                size=(self._ripple_rad, self._ripple_rad),
                pos=(
                    self.ripple_pos[0] - self._ripple_rad / 2.0,
                    self.ripple_pos[1] - self._ripple_rad / 2.0,
                ),
                group="rectangular_ripple_behavior",
            )
            StencilUnUse(group="rectangular_ripple_behavior")
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self._round_rad,
                group="rectangular_ripple_behavior",
            )
            StencilPop(group="rectangular_ripple_behavior")
        self.bind(ripple_color=self._set_color, _ripple_rad=self._set_ellipse)

    def _set_ellipse(self, instance, value):
        super()._set_ellipse(instance, value)
        self.ellipse.pos = (
            self.ripple_pos[0] - self._ripple_rad / 2.0,
            self.ripple_pos[1] - self._ripple_rad / 2.0,
        )


class CircularRippleBehavior(CommonRipple):


    ripple_scale = NumericProperty(1)


    def lay_canvas_instructions(self) -> None:
        if self._no_ripple_effect:
            return

        with self.canvas.after if self.ripple_canvas_after else self.canvas.before:
            StencilPush(group="circular_ripple_behavior")
            self.stencil = Ellipse(
                size=(
                    self.width * self.ripple_scale,
                    self.height * self.ripple_scale,
                ),
                pos=(
                    self.center_x - (self.width * self.ripple_scale) / 2,
                    self.center_y - (self.height * self.ripple_scale) / 2,
                ),
                group="circular_ripple_behavior",
            )
            StencilUse(group="circular_ripple_behavior")
            self.col_instruction = Color(rgba=self.ripple_color)
            self.ellipse = Ellipse(
                size=(self._ripple_rad, self._ripple_rad),
                pos=(
                    self.center_x - self._ripple_rad / 2.0,
                    self.center_y - self._ripple_rad / 2.0,
                ),
                group="circular_ripple_behavior",
            )
            StencilUnUse(group="circular_ripple_behavior")
            Ellipse(
                pos=self.pos, size=self.size, group="circular_ripple_behavior"
            )
            StencilPop(group="circular_ripple_behavior")
            self.bind(
                ripple_color=self._set_color, _ripple_rad=self._set_ellipse
            )

    def _set_ellipse(self, instance, value):
        super()._set_ellipse(instance, value)
        if self.ellipse.size[0] > self.width * 0.6 and not self._fading_out:
            self.fade_out()
        self.ellipse.pos = (
            self.center_x - self._ripple_rad / 2.0,
            self.center_y - self._ripple_rad / 2.0,
        )
