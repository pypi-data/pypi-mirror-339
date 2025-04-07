"""Canvas object uses these methods to draw shapes and text."""

from math import cos, sin
from typing_extensions import Self, Sequence

from ..geometry.geometry import homogenize, ellipse_point, close_points2
from ..graphics.all_enums import (
    Anchor,
    BackStyle,
    Drawable,
    FrameShape,
    PathOperation,
    Types,
    drawable_types,
)
from ..colors import colors
from ..tikz.tikz import scope_code_required
from ..graphics.sketch import (
    ArcSketch,
    BatchSketch,
    BezierSketch,
    CircleSketch,
    EllipseSketch,
    LineSketch,
    PathSketch,
    PatternSketch,
    RectSketch,
    ShapeSketch,
    TagSketch,
)
from ..settings.settings import defaults
from ..canvas.style_map import line_style_map, shape_style_map, group_args
from ..helpers.illustration import Tag
from ..graphics.shape import Shape
from ..graphics.common import Point
from ..geometry.bezier import bezier_points
from ..geometry.ellipse import elliptic_arc_points
from ..graphics.affine import rotation_matrix
from ..helpers.utilities import decompose_transformations


Color = colors.Color


def help_lines(
    self,
    pos: Point = None,
    width: float = None,
    height: float = None,
    step_size=None,
    cs_size: float = None,
    **kwargs,
):
    """
    Draw a square grid with the given size.

    Args:
        pos (Point, optional): Position of the grid. Defaults to None.
        width (float, optional): Length of the grid along the x-axis. Defaults to None.
        height (float, optional): Length of the grid along the y-axis. Defaults to None.
        step_size (optional): Step size for the grid. Defaults to None.
        cs_size (float, optional): Size of the coordinate system. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    self.grid(pos, width, height, step_size, **kwargs)
    if cs_size > 0:
        self.draw_CS(cs_size, **kwargs)
    return self


def arc(
    self,
    center: Point,
    radius_x: float,
    radius_y: float,
    start_angle: float,
    span_angle: float,
    rot_angle: float,
    n_points: int = None,
    **kwargs,
) -> None:
    """
    Draw an arc with the given center, radius, start and end angles in radians.
    Arc is drawn in counterclockwise direction from start to end.

    Args:
        center (Point): Center of the arc.
        radius_x (float): Radius of the arc.
        radius_y (float): Second radius of the arc.
        start_angle (float): Start angle of the arc in radians.
        end_angle (float): End angle of the arc in radians.

        rot_angle (float): Rotation angle of the arc.
        **kwargs: Additional keyword arguments.
    """
    if radius_y is None:
        radius_y = radius_x
    vertices = elliptic_arc_points(center, radius_x, radius_y, start_angle, span_angle, n_points)
    if rot_angle != 0:
        vertices = homogenize(vertices) @ rotation_matrix(rot_angle, center)
    self._all_vertices.extend(vertices.tolist() + [center])

    sketch = ArcSketch(
        vertices = vertices,
        xform_matrix = self.xform_matrix
    )
    for attrib_name in shape_style_map:
        if hasattr(sketch, attrib_name):
            attrib_value = self.resolve_property(sketch, attrib_name)
        else:
            attrib_value = defaults[attrib_name]
        setattr(sketch, attrib_name, attrib_value)
    for k, v in kwargs.items():
        setattr(sketch, k, v)
    self.active_page.sketches.append(sketch)

    return self


def bezier(self, control_points, **kwargs):
    """
    Draw a Bezier curve with the given control points.

    Args:
        control_points: Control points for the Bezier curve.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    self._all_vertices.extend(control_points)
    sketch = BezierSketch(control_points, self.xform_matrix)
    for attrib_name in shape_style_map:
        if hasattr(sketch, attrib_name):
            attrib_value = self._resolve_property(sketch, attrib_name)
        else:
            attrib_value = defaults[attrib_name]
        setattr(sketch, attrib_name, attrib_value)
    self.active_page.sketches.append(sketch)

    for k, v in kwargs.items():
        setattr(sketch, k, v)
    return self


def circle(self, center: Point, radius: float, **kwargs) -> None:
    """
    Draw a circle with the given center and radius.

    Args:
        center (Point): Center of the circle.
        radius (float): Radius of the circle.
        **kwargs: Additional keyword arguments.
    """
    x, y = center[:2]
    p1 = x - radius, y - radius
    p2 = x + radius, y + radius
    p3 = x - radius, y + radius
    p4 = x + radius, y - radius
    self._all_vertices.extend([p1, p2, p3, p4])
    sketch = CircleSketch(center, radius, self.xform_matrix)
    for attrib_name in shape_style_map:
        if hasattr(sketch, attrib_name):
            attrib_value = self.resolve_property(sketch, attrib_name)
        else:
            attrib_value = defaults[attrib_name]
        setattr(sketch, attrib_name, attrib_value)
    for k, v in kwargs.items():
        setattr(sketch, k, v)
    self.active_page.sketches.append(sketch)

    return self


def ellipse(self, center: Point, width: float, height, angle, **kwargs) -> None:
    """
    Draw an ellipse with the given center and x_radius and y_radius.

    Args:
        center (Point): Center of the ellipse.
        width (float): Width of the ellipse.
        height: Height of the ellipse.
        angle: Angle of the ellipse.
        **kwargs: Additional keyword arguments.
    """
    x, y = center[:2]
    x_radius = width / 2
    y_radius = height / 2
    p1 = x - x_radius, y - y_radius
    p2 = x + x_radius, y + y_radius
    p3 = x - x_radius, y + y_radius
    p4 = x + x_radius, y - y_radius
    self._all_vertices.extend([p1, p2, p3, p4])
    sketch = EllipseSketch(center, x_radius, y_radius, angle, self.xform_matrix)
    for attrib_name in shape_style_map:
        if hasattr(sketch, attrib_name):
            attrib_value = self.resolve_property(sketch, attrib_name)
        else:
            attrib_value = defaults[attrib_name]
        setattr(sketch, attrib_name, attrib_value)
    for k, v in kwargs.items():
        setattr(sketch, k, v)
    self.active_page.sketches.append(sketch)

    return self


def text(
    self,
    txt: str,
    pos: Point,
    font_family: str = None,
    font_size: int = None,
    font_color: Color = None,
    anchor: Anchor = None,
    **kwargs,
) -> None:
    """
    Draw the given text at the given position.

    Args:
        txt (str): Text to be drawn.
        pos (Point): Position of the text.
        font_family (str, optional): Font family of the text. Defaults to None.
        font_size (int, optional): Font size of the text. Defaults to None.
        font_color (Color, optional): Font color of the text. Defaults to None.
        anchor (Anchor, optional): Anchor of the text. Defaults to None.
        **kwargs: Additional keyword arguments.
    """
    # first create a Tag object
    tag_obj = Tag(
        txt,
        pos,
        font_family=font_family,
        font_size=font_size,
        font_color=font_color,
        anchor=anchor,
        **kwargs,
    )
    tag_obj.draw_frame = False
    # then call get_tag_sketch to create a TagSketch object
    sketch = create_sketch(tag_obj, self, **kwargs)
    self.active_page.sketches.append(sketch)

    return self


def line(self, start, end, **kwargs):
    """
    Draw a line segment from start to end.

    Args:
        start: Starting point of the line.
        end: Ending point of the line.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    line_shape = Shape([start, end], closed=False, **kwargs)
    line_sketch = create_sketch(line_shape, self, **kwargs)
    self.active_page.sketches.append(line_sketch)

    return self


def rectangle(self, center: Point, width: float, height: float, angle: float, **kwargs):
    """
    Draw a rectangle with the given center, width, height and angle.

    Args:
        center (Point): Center of the rectangle.
        width (float): Width of the rectangle.
        height (float): Height of the rectangle.
        angle (float): Angle of the rectangle.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    w2 = width / 2
    h2 = height / 2
    p1 = center[0] - w2, center[1] + h2
    p2 = center[0] - w2, center[1] - h2
    p3 = center[0] + w2, center[1] - h2
    p4 = center[0] + w2, center[1] + h2
    points = homogenize([p1, p2, p3, p4]) @ rotation_matrix(angle, center)
    rect_shape = Shape(points.tolist(), closed=True, **kwargs)
    rect_sketch = create_sketch(rect_shape, self, **kwargs)
    self.active_page.sketches.append(rect_sketch)

    return self


def draw_CS(self, size: float = None, **kwargs):
    """
    Draw a coordinate system with the given size.

    Args:
        size (float, optional): Size of the coordinate system. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    if size is None:
        size = defaults["CS_size"]
    if "colors" in kwargs:
        x_color, y_color = kwargs["colors"]
        del kwargs["colors"]
    else:
        x_color = defaults["CS_x_color"]
        y_color = defaults["CS_y_color"]
    if "line_width" not in kwargs:
        kwargs["line_width"] = defaults["CS_line_width"]
    self.line((0, 0), (size, 0), line_color=x_color, **kwargs)
    self.line((0, 0), (0, size), line_color=y_color, **kwargs)
    if "line_color" not in kwargs:
        kwargs["line_color"] = defaults["CS_origin_color"]
    self.circle((0, 0), radius=defaults["CS_origin_size"], **kwargs)

    return self


def lines(self, points, **kwargs):
    """
    Draw connected line segments.

    Args:
        points: Points to be connected.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    self._all_vertices.extend(points)
    sketch = LineSketch(points, self.xform_matrix, **kwargs)
    for attrib_name in line_style_map:
        attrib_value = self._resolve_property(sketch, attrib_name)
        setattr(sketch, attrib_name, attrib_value)
    self.active_page.sketches.append(sketch)

    return self


def draw_bbox(self, bbox, **kwargs):
    """
    Draw the bounding box object.

    Args:
        bbox: Bounding box to be drawn.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    sketch = create_sketch(bbox, self, **kwargs)
    self.active_page.sketches.append(sketch)

    return self


def draw_pattern(self, pattern, **kwargs):
    """
    Draw the pattern object.

    Args:
        pattern: Pattern object to be drawn.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    sketch = create_sketch(pattern, self, **kwargs)
    self.active_page.sketches.append(sketch)

    return self


def draw_hobby(
    self,
    points: Sequence[Point],
    controls: Sequence[Point],
    cyclic: bool = False,
    **kwargs
):
    """Draw a Hobby curve through the given points using the control points.

    Args:
        points (Sequence[Point]): Points through which the curve passes.
        controls (Sequence[Point]): Control points for the curve.
        cyclic (bool, optional): Whether the curve is cyclic. Defaults to False.
        **kwargs: Additional keyword arguments.
    """
    n = len(points)
    if cyclic:
        for i in range(n):
            ind = i * 2
            bezier_pnts = bezier_points(
                points[i], *controls[ind : ind + 2], points[(i + 1) % n], 20
            )
            bezier_ = Shape(bezier_pnts)
            self.draw(bezier_, **kwargs)
    else:
        for i in range(len(points) - 1):
            ind = i * 2
            bezier_pnts = bezier_points(
                points[i], *controls[ind : ind + 2], points[i + 1], 20
            )
            bezier_ = Shape(bezier_pnts)
            self.draw(bezier_, **kwargs)


def draw_lace(self, lace, **kwargs):
    """Draw the lace object.

    Args:
        lace: Lace object to be drawn.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    keys = list(lace.fragment_groups.keys())
    keys.sort()
    if lace.swatch is not None:
        n_colors = len(lace.swatch)
    for i, key in enumerate(keys):
        if lace.swatch is not None:
            fill_color = colors.Color(*lace.swatch[i % n_colors])
            kwargs["fill_color"] = fill_color
        for fragment in lace.fragment_groups[key]:
            self.active_page.sketches.append(create_sketch(fragment, self, **kwargs))
    for plait in lace.plaits:
        if lace.swatch is not None:
            fill_color = colors.white
            kwargs["fill_color"] = fill_color
        else:
            kwargs["fill_color"] = None
        self.active_page.sketches.append(create_sketch(plait, self, **kwargs))
        self._all_vertices.extend(plait.corners)

    return self


def draw_dimension(self, item, **kwargs):
    """Draw the dimension object.

    Args:
        item: Dimension object to be drawn.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    for shape in item.all_shapes:
        self._all_vertices.extend(shape.corners)
    for ext in [item.ext1, item.ext2, item.ext3]:
        if ext:
            ext_sketch = create_sketch(ext, self, **kwargs)
            self.active_page.sketches.append(ext_sketch)
    if item.dim_line:
        dim_sketch = create_sketch(item.dim_line, self, **kwargs)
        self.active_page.sketches.extend(dim_sketch)
    if item.arrow1:
        arrow_sketch = create_sketch(item.arrow1, self, **kwargs)
        self.active_page.sketches.extend(arrow_sketch)
        self.active_page.sketches.append(create_sketch(item.mid_line, self))
    if item.arrow2:
        arrow_sketch = create_sketch(item.arrow2, self, **kwargs)
        self.active_page.sketches.extend(arrow_sketch)
    x, y = item.text_pos[:2]

    tag = Tag(item.text, (x, y), font_size=item.font_size, **kwargs)
    tag_sketch = create_sketch(tag, self, **kwargs)
    tag_sketch.draw_frame = True
    tag_sketch.frame_shape = FrameShape.CIRCLE
    tag_sketch.fill = True
    tag_sketch.font_color = colors.black
    tag_sketch.frame_back_style = BackStyle.COLOR
    tag_sketch.back_style = BackStyle.COLOR
    tag_sketch.frame_back_color = colors.white
    tag_sketch.back_color = colors.white
    tag_sketch.stroke = False
    self.active_page.sketches.append(tag_sketch)

    return self


def grid(
    self, pos=(0, 0), width: float = None, height: float = None, step_size=None, **kwargs
):
    """Draw a square grid with the given size.

    Args:
        pos (tuple, optional): Position of the grid. Defaults to (0, 0).
        width (float, optional): Length of the grid along the x-axis. Defaults to None.
        height (float, optional): Length of the grid along the y-axis. Defaults to None.
        step_size (optional): Step size for the grid. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    x, y = pos[:2]
    if width is None:
        width = defaults["grid_size"]
        height = defaults["grid_size"]
    if "line_width" not in kwargs:
        kwargs["line_width"] = defaults["grid_line_width"]
    if "line_color" not in kwargs:
        kwargs["line_color"] = defaults["grid_line_color"]
    if "line_dash_array" not in kwargs:
        kwargs["line_dash_array"] = defaults["grid_line_dash_array"]
    # draw x-axis
    # self.line((-size, 0), (size, 0), **kwargs)
    line_y = Shape([(x, y), (x + width, y)], **kwargs)
    line_x = Shape([(x, y), (x, y + height)], **kwargs)
    lines_x = line_y.translate(0, step_size, reps=int(height / step_size))
    lines_y = line_x.translate(step_size, 0, reps=int(width / step_size))
    self.draw(lines_x)
    self.draw(lines_y)
    return self


regular_sketch_types = [
    Types.ARC,
    Types.ARC_ARROW,
    Types.BATCH,
    Types.BEZIER,
    Types.CIRCLE,
    Types.DIVISION,
    Types.DOT,
    Types.DOTS,
    Types.ELLIPSE,
    Types.FRAGMENT,
    Types.OUTLINE,
    Types.OVERLAP,
    Types.PARALLEL_POLYLINE,
    Types.PATH,
    Types.PLAIT,
    Types.POLYLINE,
    Types.Q_BEZIER,
    Types.RECTANGLE,
    Types.SECTION,
    Types.SEGMENT,
    Types.SHAPE,
    Types.SINE_WAVE,
    Types.STAR,
    Types.TAG,
]


def extend_vertices(canvas, item):
    """Extend the list of all vertices with the vertices of the given item.

    Args:
        canvas: Canvas object.
        item: Item whose vertices are to be extended.
    """
    all_vertices = canvas._all_vertices
    if item.subtype == Types.DOTS:
        vertices = [x.pos for x in item.all_shapes]
        vertices = [x[:2] for x in homogenize(vertices) @ canvas._xform_matrix]
        all_vertices.extend(vertices)
    elif item.subtype == Types.DOT:
        vertices = [item.pos]
        vertices = [x[:2] for x in homogenize(vertices) @ canvas._xform_matrix]
        all_vertices.extend(vertices)
    elif item.subtype == Types.ARROW:
        for shape in item.all_shapes:
            all_vertices.extend(shape.corners)
    elif item.subtype == Types.LACE:
        for plait in item.plaits:
            all_vertices.extend(plait.corners)
        for fragment in item.fragments:
            all_vertices.extend(fragment.corners)
    elif item.subtype == Types.PATTERN:
        all_vertices.extend(item.get_all_vertices())
    else:
        corners = [x[:2] for x in homogenize(item.corners) @ canvas._xform_matrix]
        all_vertices.extend(corners)


def draw(self, item: Drawable, **kwargs) -> Self:
    """The item is drawn on the canvas with the given style properties.

    Args:
        item (Drawable): Item to be drawn.
        **kwargs: Additional keyword arguments.

    Returns:
        Self: The canvas object.
    """
    # check if the item has any points
    if not item:
        return self

    active_sketches = self.active_page.sketches
    subtype = item.subtype
    extend_vertices(self, item)
    if subtype in regular_sketch_types:
        sketches = get_sketches(item, self, **kwargs)
        if sketches:
            active_sketches.extend(sketches)
    elif subtype == Types.PATTERN:
        draw_pattern(self, item, **kwargs)
    elif subtype == Types.DIMENSION:
        self.draw_dimension(item, **kwargs)
    elif subtype == Types.ARROW:
        for head in item.heads:
            active_sketches.append(create_sketch(head, self, **kwargs))
        active_sketches.append(create_sketch(item.line, self, **kwargs))
    elif subtype == Types.LACE:
        self.draw_lace(item, **kwargs)
    elif subtype == Types.BOUNDING_BOX:
        draw_bbox(self, item, **kwargs)
    return self


def get_sketches(item: Drawable, canvas: "Canvas" = None, **kwargs) -> list["Sketch"]:
    """Create sketches from the given item and return them as a list.

    Args:
        item (Drawable): Item to be sketched.
        canvas (Canvas, optional): Canvas object. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        list[Sketch]: List of sketches.
    """
    if not (item.visible and item.active):
        res = []
    elif item.subtype in drawable_types:
        sketches = create_sketch(item, canvas, **kwargs)
        if isinstance(sketches, list):
            res = sketches
        elif sketches is not None:
            res = [sketches]
        else:
            res = []
    else:
        res = []
    return res


def set_shape_sketch_style(sketch, item, canvas, linear=False, **kwargs):
    """Set the style properties of the sketch.

    Args:
        sketch: Sketch object.
        item: Item whose style properties are to be set.
        canvas: Canvas object.
        linear (bool, optional): Whether the style is linear. Defaults to False.
        **kwargs: Additional keyword arguments.
    """
    if linear:
        style_map = line_style_map
    else:
        style_map = shape_style_map

    for attrib_name in style_map:
        attrib_value = canvas._resolve_property(item, attrib_name)
        setattr(sketch, attrib_name, attrib_value)

    sketch.visible = item.visible
    sketch.active = item.active
    sketch.closed = item.closed
    sketch.fill = item.fill
    sketch.stroke = item.stroke

    for k, v in kwargs.items():
        setattr(sketch, k, v)


def create_sketch(item, canvas, **kwargs):
    """Create a sketch from the given item.

    Args:
        item: Item to be sketched.
        canvas: Canvas object.
        **kwargs: Additional keyword arguments.

    Returns:
        Sketch: Created sketch.
    """
    if not (item.visible and item.active):
        return None

    def get_tag_sketch(item, canvas, **kwargs):
        """Create a TagSketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            TagSketch: Created TagSketch.
        """
        pos = item.pos
        # pos = [(round(pos[0], nround), round(pos[1], nround))]
        sketch = TagSketch(text=item.text, pos=pos, anchor=item.anchor)
        for attrib_name in item._style_map:
            if attrib_name == "fill_color":
                if item.fill_color in [None, colors.black]:
                    setattr(sketch, "frame_back_color", defaults["frame_back_color"])
                else:
                    setattr(sketch, "frame_back_color", item.fill_color)
                continue
            attrib_value = canvas._resolve_property(item, attrib_name)
            setattr(sketch, attrib_name, attrib_value)
        sketch.text_width = item.text_width
        sketch.visible = item.visible
        sketch.active = item.active
        for k, v in kwargs.items():
            setattr(sketch, k, v)
        return sketch

    def get_ellipse_sketch(item, canvas, **kwargs):
        """Create an EllipseSketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            EllipseSketch: Created EllipseSketch.
        """
        sketch = EllipseSketch(
            item.center, item.a, item.b, item.angle, xform_matrix=canvas.xform_matrix
        )
        set_shape_sketch_style(sketch, item, canvas, **kwargs)

        return sketch

    def get_pattern_sketch(item, canvas, **kwargs):
        """Create a PatternSketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            PatternSketch: Created PatternSketch.
        """
        sketch = PatternSketch(item, xform_matrix=canvas.xform_matrix)
        set_shape_sketch_style(sketch, item, canvas, **kwargs)

        return sketch

    def get_circle_sketch(item, canvas, **kwargs):
        """Create a CircleSketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            CircleSketch: Created CircleSketch.
        """
        sketch = CircleSketch(
            item.center, item.radius, xform_matrix=canvas.xform_matrix
        )
        set_shape_sketch_style(sketch, item, canvas, **kwargs)

        return sketch

    def get_dots_sketch(item, canvas, **kwargs):
        """Create sketches for dots from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            list: List of created sketches.
        """
        vertices = [x.pos for x in item.all_shapes]
        fill_color = item[0].fill_color
        radius = item[0].radius
        marker_size = item[0].marker_size
        marker_type = item[0].marker_type
        item = Shape(
            vertices,
            fill_color=fill_color,
            markers_only=True,
            draw_markers=True,
            marker_size=marker_size,
            marker_radius=radius,
            marker_type=marker_type,
        )
        sketches = get_sketches(item, canvas, **kwargs)

        return sketches

    def get_arc_sketch(item, canvas, **kwargs):
        """Create an ArcSketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            ArcSketch: Created ArcSketch.
        """
        sketch = ArcSketch(
            item.vertices,
            xform_matrix=canvas.xform_matrix
        )
        set_shape_sketch_style(sketch, item, canvas, **kwargs)

        return sketch

    def get_lace_sketch(item, canvas, **kwargs):
        """Create sketches for lace from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            list: List of created sketches.
        """
        sketches = [get_sketch(frag, canvas, **kwargs) for frag in item.fragments]
        sketches.extend([get_sketch(plait, canvas, **kwargs) for plait in item.plaits])
        return sketches

    def get_batch_sketch(item, canvas, **kwargs):
        """Create a BatchSketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            BatchSketch or list: Created BatchSketch or list of sketches.
        """
        if scope_code_required(item):
            sketches = []
            for element in item.elements:
                if element.visible and element.active:
                    sketches.extend(get_sketches(element, canvas, **kwargs))

            sketch = BatchSketch(sketches=sketches)
            for arg in group_args:
                setattr(sketch, arg, getattr(item, arg))

            res = sketch
        else:
            sketches = []
            for element in item.elements:
                if element.visible and element.active:
                    sketches.extend(get_sketches(element, canvas, **kwargs))

            res = sketches

        return res

    def get_path_sketch(item, canvas, **kwargs):
        """Create sketches for a path from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            list: List of created sketches.
        """
        def extend_verts(obj, vertices):
            obj_vertices = obj.vertices
            if obj_vertices:
                if vertices and close_points2(vertices[-1], obj_vertices[0]):
                    obj_vertices = obj_vertices[1:]
                vertices.extend(obj_vertices)

        path_op = PathOperation
        linears = [path_op.ARC,
                    path_op.ARC_TO,
                    path_op.BLEND_ARC,
                    path_op.BLEND_CUBIC,
                    path_op.BLEND_QUAD,
                    path_op.BLEND_SINE,
                    path_op.CUBIC_TO,
                    path_op.FORWARD,
                    path_op.H_LINE,
                    path_op.HOBBY_TO,
                    path_op.QUAD_TO,
                    path_op.R_LINE,
                    path_op.SEGMENTS,
                    path_op.SINE,
                    path_op.V_LINE,
                    path_op.LINE_TO]
        sketches = []
        vertices = []
        for i, op in enumerate(item.operations):
            if op.subtype in linears:
                obj = item.objects[i]
                extend_verts(obj, vertices)
            elif op.subtype in [path_op.MOVE_TO, path_op.R_MOVE]:
                if i == 0:
                    continue
                shape = Shape(vertices)
                sketch = create_sketch(shape, canvas, **kwargs)
                if sketch:
                    sketch.visible = item.visible
                    sketch.active = item.active
                    sketches.append(sketch)
                vertices = []
            elif op.subtype == path_op.CLOSE:
                shape = Shape(vertices, closed=True)
                sketch = create_sketch(shape, canvas, **kwargs)
                if sketch:
                    sketch.visible = item.visible
                    sketch.active = item.active
                    sketches.append(sketch)
                vertices = []
        if vertices:
            shape = Shape(vertices)
            sketch = create_sketch(shape, canvas, **kwargs)
            sketches.append(sketch)

        if 'handles' in kwargs and kwargs['handles']:
            handles = kwargs['handles']
            del kwargs['handles']
            for handle in item.handles:
                shape = Shape(handle)
                shape.subtype = Types.HANDLE
                handle_sketches = create_sketch(shape, canvas, **kwargs)
                sketches.extend(handle_sketches)

        for sketch in sketches:
            item.closed = sketch.closed
            set_shape_sketch_style(sketch, item, canvas, **kwargs)

        return sketches

    def get_bbox_sketch(item, canvas, **kwargs):
        """Create a bounding box sketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            ShapeSketch: Created bounding box sketch.
        """
        nround = defaults["tikz_nround"]
        vertices = [(round(x[0], nround), round(x[1], nround)) for x in item.corners]
        if not vertices:
            return None
        sketch = ShapeSketch(vertices, canvas._xform_matrix)
        sketch.subtype = Types.BBOX_SKETCH
        sketch.visible = True
        sketch.active = True
        sketch.closed = True
        sketch.fill = False
        sketch.stroke = True
        sketch.line_color = colors.gray
        sketch.line_width = 1
        sketch.line_dash_array = [3, 3]
        sketch.draw_markers = False
        return sketch

    def get_handle_sketch(item, canvas, **kwargs):
        """Create handle sketches from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            list: List of created handle sketches.
        """
        nround = defaults["tikz_nround"]
        vertices = [(round(x[0], nround), round(x[1], nround)) for x in item.vertices]
        if not vertices:
            return None
        sketches = []
        sketch = ShapeSketch(vertices, canvas._xform_matrix)
        sketch.subtype = Types.HANDLE
        sketch.closed = False
        set_shape_sketch_style(sketch, item, canvas, **kwargs)
        sketches.append(sketch)
        temp_item = Shape()
        temp_item.closed = True
        handle1 = RectSketch(item.vertices[0], 3, 3, canvas._xform_matrix)
        set_shape_sketch_style(handle1, temp_item, canvas, **kwargs)
        handle2 = RectSketch(item.vertices[-1], 3, 3, canvas._xform_matrix)
        set_shape_sketch_style(handle2, temp_item, canvas, **kwargs)
        sketches.extend([handle1, handle2])

        return sketches

    def get_sketch(item, canvas, **kwargs):
        """Create a sketch from the given item.

        Args:
            item: Item to be sketched.
            canvas: Canvas object.
            **kwargs: Additional keyword arguments.

        Returns:
            ShapeSketch: Created sketch.
        """
        nround = defaults["tikz_nround"]
        vertices = [
            (round(x[0], nround), round(x[1], nround)) for x in item.final_coords
        ]
        if not vertices:
            return None
        sketch = ShapeSketch(vertices, canvas._xform_matrix)
        set_shape_sketch_style(sketch, item, canvas, **kwargs)

        return sketch



    d_subtype_sketch = {
        Types.ARC: get_arc_sketch,
        Types.ARC_ARROW: get_batch_sketch,
        Types.ARROW: get_batch_sketch,
        Types.ARROW_HEAD: get_sketch,
        Types.BATCH: get_batch_sketch,
        Types.BEZIER: get_sketch,
        Types.BOUNDING_BOX: get_bbox_sketch,
        Types.CIRCLE: get_circle_sketch,
        Types.DIVISION: get_sketch,
        Types.DOT: get_circle_sketch,
        Types.DOTS: get_dots_sketch,
        Types.ELLIPSE: get_sketch,
        Types.FRAGMENT: get_sketch,
        Types.HANDLE: get_handle_sketch,
        Types.LACE: get_lace_sketch,
        Types.OVERLAP: get_batch_sketch,
        Types.PARALLEL_POLYLINE: get_batch_sketch,
        Types.PATH: get_path_sketch,
        Types.PATTERN: get_pattern_sketch,
        Types.PLAIT: get_sketch,
        Types.POLYLINE: get_sketch,
        Types.Q_BEZIER: get_sketch,
        Types.RECTANGLE: get_sketch,
        Types.SECTION: get_sketch,
        Types.SEGMENT: get_sketch,
        Types.SHAPE: get_sketch,
        Types.SINE_WAVE: get_sketch,
        Types.STAR: get_batch_sketch,
        Types.TAG: get_tag_sketch,
    }

    return d_subtype_sketch[item.subtype](item, canvas, **kwargs)
