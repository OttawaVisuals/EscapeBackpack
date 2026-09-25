// Norse adventure keepsake medallion — printable two-piece version.
// Print FRONT and BACK face-up, then glue the flat backs together.
// The assembled medallion is 50 mm diameter x 4.4 mm thick.

DIAMETER = 50;
CORE = 1.6;
RELIEF = 0.6;
$fn = 96;
PART = "comparison"; // set to "front" or "back" for slicer export

module coin_rim() {
    difference() {
        circle(d=48.4);
        circle(d=46.8);
    }
}

module shield_outer() {
    polygon([[-14,14],[-11.5,17],[11.5,17],[14,14],[14,-5],[0,-17],[-14,-5]]);
}

module shield_inner() {
    polygon([[-12.7,13.5],[-10.8,15.5],[10.8,15.5],[12.7,13.5],[12.7,-4.7],[0,-15.2],[-12.7,-4.7]]);
}

module raven_profile() {
    difference() {
        polygon([
            [-12.0,3.2], [-8.6,4.0], [-5.4,4.0], [-3.0,7.5],
            [-0.2,9.0], [2.7,8.2], [4.6,6.0], [4.0,4.0],
            [7.4,2.6], [10.6,0.1], [11.0,-6.4], [5.5,-4.3],
            [2.6,-5.1], [0.2,-3.8], [-2.6,-7.0], [-5.9,-6.3],
            [-4.4,-3.4], [-8.0,-2.1], [-6.2,0.0], [-10.1,0.7]
        ]);
        // Small eye and broad wing break expose the flat coin face below.
        translate([-1.0,6.0]) circle(d=1.05);
        polygon([[-5.6,2.3],[-2.0,3.0],[2.0,1.4],[5.2,-0.2],[3.4,-1.7],[-0.2,-0.6],[-3.5,0.0]]);
    }
}

module front_relief() {
    union() {
        coin_rim();
        difference() {
            shield_outer();
            shield_inner();
        }
        raven_profile();
    }
}

module compass_rose() {
    // Four bold cardinal points with shorter diagonal points.
    polygon([
        [0,8.5],[1.0,2.4],[3.5,3.5],[2.4,1.0],
        [8.5,0],[2.4,-1.0],[3.5,-3.5],[1.0,-2.4],
        [0,-8.5],[-1.0,-2.4],[-3.5,-3.5],[-2.4,-1.0],
        [-8.5,0],[-2.4,1.0],[-3.5,3.5],[-1.0,2.4]
    ]);
}

module bold_text(label, size) {
    // A light offset strengthens small bold letter strokes for the 0.4 mm nozzle.
    offset(r=0.0)
        text(label, size=size, font="Arial:style=Bold", halign="center", valign="center", spacing=1.0);
}

module back_relief() {
    union() {
        coin_rim();
        translate([0,13.0]) bold_text("ADVENTURE", 5.0);
        translate([0,-11.3]) bold_text("COMPLETE", 5.0);
        compass_rose();
        // Compact shared maker mark. Kept as text so the reverse can be reused.
        translate([0,-17.7]) bold_text("ESCAPE", 2.6);
        translate([0,-20.5]) bold_text("BACKPACK", 2.6);
    }
}

module front_part() {
    union() {
        cylinder(d=DIAMETER, h=CORE);
        translate([0,0,CORE]) linear_extrude(height=RELIEF) front_relief();
    }
}

module back_part() {
    union() {
        cylinder(d=DIAMETER, h=CORE);
        translate([0,0,CORE]) linear_extrude(height=RELIEF) back_relief();
    }
}

module assembled_view() {
    // The two flat backs meet at z=0; glue them there.
    color([0.67,0.70,0.72]) front_part();
    color([0.78,0.70,0.53]) rotate([180,0,0]) back_part();
}

module preview_front() {
    // Contrasting shades separate relief from blank in the preview only.
    color([0.49,0.52,0.54]) cylinder(d=DIAMETER, h=CORE);
    color([0.82,0.85,0.86]) translate([0,0,CORE]) linear_extrude(height=RELIEF) front_relief();
}

module preview_back() {
    color([0.64,0.55,0.36]) cylinder(d=DIAMETER, h=CORE);
    color([0.90,0.80,0.60]) translate([0,0,CORE]) linear_extrude(height=RELIEF) back_relief();
}

module comparison_view() {
    // Both printable halves face upward for an easy design comparison.
    translate([-27,0,0]) preview_front();
    translate([27,0,0]) preview_back();
}

if (PART == "front") front_part();
else if (PART == "back") back_part();
else if (PART == "assembly") assembled_view();
else comparison_view();


