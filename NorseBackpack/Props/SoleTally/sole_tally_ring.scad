// SOLE treasure tally: replacement counter ring with our own seven-segment digits.
// Reuses the click mechanism of the reference ring (reference/4-digit_counter.3mf,
// extracted by build_sole_tally.py) and only replaces the numerals.
//
// Digits are strict seven-segment so the tally shows 3705 and, turned 180 degrees,
// reads SOLE (3->E, 7->L, 0->O, 5->S). The reference ring's 7 had a slanted stroke
// that broke the L.
//
// PART = "ring"  : ring body with digits cut in (print colour 1)
// PART = "inlay" : digits only, flush with the face (print colour 2, same object)
// PART = "both"  : preview of both, inlay coloured

PART = "both";

// Digit size on each face (mm). Face is ~7.4 mm wide, band zone is 4.5 mm tall.
DIGIT_H = 5.6;      // along the ring's rotation direction
DIGIT_W = 3.4;      // along the ring's axis
STROKE  = 0.7;
DIGIT_Z = -0.25;    // centre offset along the axis, matches the reference digit band

// Reference ring geometry (measured from the 3MF).
R_OUTER   = 12.0;   // decagon circumradius, vertex at 0 degrees
CUT_FLOOR = 10.85;  // digit floor distance from centre (reference cut depth ~0.55 mm)
FILL_IN   = 10.4;   // inner edge of the shell that fills the old digits
FILL_Z    = [-2.5, 2.0];
// The fill shell stands 0.02 mm proud of the old faces: a shell exactly coplanar with the
// body leaves non-manifold edges in OpenSCAD 2021 (CGAL). 0.02 mm is below print resolution.
FILL_R    = R_OUTER + 0.02;
FACE      = FILL_R * cos(18);   // outer face of the digit zone

// Seven segments in digit coordinates: x = right, y = up.
module seg(s) {
    w = DIGIT_W; h = DIGIT_H; t = STROKE;
    if (s == "a") translate([-w/2,  h/2 - t]) square([w, t]);
    if (s == "b") translate([ w/2 - t, 0])   square([t, h/2]);
    if (s == "c") translate([ w/2 - t, -h/2]) square([t, h/2]);
    if (s == "d") translate([-w/2, -h/2])    square([w, t]);
    if (s == "e") translate([-w/2, -h/2])    square([t, h/2]);
    if (s == "f") translate([-w/2, 0])       square([t, h/2]);
    if (s == "g") translate([-w/2, -t/2])    square([w, t]);
}

SEGMENTS = ["abcdef", "bc", "abged", "abgcd", "fgbc",
            "afgcd", "afgedc", "abc", "abcdefg", "abcdfg"];

module digit2d(v) {
    segs = SEGMENTS[v];
    union() for (i = [0 : len(segs) - 1]) seg(segs[i]);
}

// Place digit v on its face. Reference layout: face k (centred at 18+36k degrees)
// carries digit 9-k; digit "up" points clockwise, digit "right" points along +Z.
module placed_digit(v, depth_from, depth_to) {
    k = 9 - v;
    rotate([0, 0, 18 + 36 * k])
        translate([depth_from, 0, DIGIT_Z])
            multmatrix([[0, 0, 1, 0], [0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
                linear_extrude(height = depth_to - depth_from)
                    digit2d(v);
}

module blank_ring() {
    union() {
        import("reference/counterring_body.stl", convexity = 10);
        translate([0, 0, FILL_Z[0]])
            difference() {
                cylinder(h = FILL_Z[1] - FILL_Z[0], r = FILL_R, $fn = 10);
                translate([0, 0, -1]) cylinder(h = 10, r = FILL_IN / cos(18), $fn = 10);
            }
    }
}

module ring() {
    difference() {
        blank_ring();
        for (v = [0 : 9]) placed_digit(v, CUT_FLOOR, R_OUTER + 1);
    }
}

module inlay() {
    for (v = [0 : 9]) placed_digit(v, CUT_FLOOR, FACE);
}

if (PART == "ring") ring();
if (PART == "inlay") inlay();
if (PART == "both") { color("gold") ring(); color("black") inlay(); }
