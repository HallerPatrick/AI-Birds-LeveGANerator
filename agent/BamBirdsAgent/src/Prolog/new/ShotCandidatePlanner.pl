%% 2DO
%% - schwarzer vogel nahe an schwein bringen, auch wenn Hill dazwischen
%% - Turm anstossen, wenn schweine nahe am rand liegen und herunterkullern
%%   koennen
%% - Eis-Stütze in Level 10 (höhere Konfidenz bei 'einmaligen' chancen)
%% - konfidenz boosten, wenn mehrere gründe für ein Target sprechen




%% Helpers


num_of_pigs_remaining(N) :-
    findall(P,pig(P),Pigs), length(Pigs,N).

num_of_birds_remaining(N) :-
    findall(B,bird(B),Birds), length(Birds,N).


% identify objects that are worth shooting at
is_goal(Object, 1.0) :-
    pig(Object,_,_,_,_).

is_goal(Object, 0.8) :-
    hasMaterial(Object, tnt, _, _, _, _).

is_goal(Object, 0.6) :-
    hasForm(Object,ball).


%% Helpers

isOnGroundOrHill(Object) :- %% FIXME: objects can be on(Obj,ground). (use on_groundlike below!!)
    (hill(Hill),
    isOn(Object, Hill));
    \+isOn(Object, _).

%Fallback isOn/2 for legacy compatibility
%isOn(Object,hill) :-
%    isOn(Object,hill,_).

%% TODO: WIP Placeholder for potential Slope detection
%isOnSlope(Object, Direction) :-
%	hill(Hill),
%	isOn(Object, Hill),

%	.

% compute bounding box for lists of objects
% boundingBox(+List_of_Objects, -Xmin, -Ymin, -Xmax, -Ymax)
bounding_box_lst([Object],X0,Y0,X1,Y1) :-
    hasMaterial(Object,_,X0,Y0,W,H),
    X1 is X0 + W,
    Y1 is Y0 - H.

bounding_box_lst([Object|OS],X0,Y0,X1,Y1) :-
    bounding_box_lst(OS,X0_Temp, Y0_Temp, X1_Temp, Y1_Temp),
    hasMaterial(Object, _, X0_O, Y0_O, W, H),
    X0 is min(X0_O,X0_Temp),
    Y0 is min(Y0_O,Y0_Temp),
    X1 is max(X1_Temp, X0_O+W),
    Y1 is max(Y1_Temp, Y0_O+H).

% checks containment of point in bounding box
point_contained(X,Y,X0,Y0,X1,Y1) :-
    between(X0,X1,X),
    between(Y0,Y1,Y).

% check containment of pig in structure
% structure_protects_big(+Struct, +Pig)
structure_bounding_box(Struct, X0, Y0, X1, Y1) :-
    findall(O, belongsTo(O,Struct), Objects),
    bounding_box_lst(Objects,X0,Y0,X1,Y1).

on_groundlike(Object) :-
    isOn(Object,ground).

on_groundlike(Object) :-
    isOn(Object, Support),
    hill(Support,_,_,_,_).

boxes_overlap(XA0, YA0, XA1, YA1, XB0, YB0, XB1, YB1) :-
    (between(XA0, XA1, XB0) ; between(XA0, XA1, XB1) ; between(XB0, XB1, XA0) ; between(XB0, XB1, XA0)), !,
    (between(YA0, YA1, YB0) ; between(YA0, YA1, YB1) ; between(YB0, YB1, YA0) ; between(YB0, YB1, YA0)), !.

in_vertical_corridor(Obj, XMin, Xmax, Ymin, Ymax) :-
    hasMaterial(Obj,_,X,Y,W,H),
    X2 is X + W,
    Y2 is Y + H,
    boxes_overlap(XMin, Ymin, Xmax, Ymax, X, Y, X2, Y2).

isLowInStructure(Object) :-
    on_groundlike(AnotherObject),
    isOn(Object, AnotherObject).

% This function will check if a given object is in front of another (Object1 left or Object2 right)
% isInFront_(+Target, +Object)
isInFront(Object1, Object2) :-
    isLeft(Object1, Object2);
    isRight(Object2, Object1).

hill(H) :-
    hill(H,_,_,_,_).

pig(P) :-
    pig(P,_,_,_,_).

hasMaterial(O,M) :-
    hasMaterial(O,M,_,_,_,_).

% defines birds
redbird(Bird) :-
	hasColor(Bird, red).

yellowbird(Bird) :-
	hasColor(Bird, yellow).

bluebird(Bird) :-
	hasColor(Bird, blue).

blackbird(Bird) :-
	hasColor(Bird, black).

whitebird(Bird) :-
	hasColor(Bird, white).

% Proper structure: a structure with at least three objects belonging to it
% isProperStructure_(+Structure)
isProperStructure(Structure) :-
    aggregate_all(count, belongsTo(_,Structure), N),
    N >= 3.

% in_slingshot(+Bird)
in_slingshot(Bird) :-
    birdOrder(Bird, 0).

%% Rough estimate for number of objects of a certain material that a certain type of bird can penetrate
% (mass * damage_multiplier * velocity_multiplier) / defense

bird_type_impact(red, wood, 217.9). % * 5444.76
bird_type_impact(red, ice, 272.4).
bird_type_impact(red, snow, 54.5).
bird_type_impact(red, stone, 36.3).
%bird_type_impact(red, tnt, 5). 217.904 272.38 54.476 36.31915
%bird_type_impact(red, pork, 10).

bird_type_impact(yellow, wood, 2*3241.1). % 4823.04 (3241.0828 2893.8242 385.8432 694.51776)
bird_type_impact(yellow, ice, 2*2893.8).
bird_type_impact(yellow, stone, 2*385.8).
bird_type_impact(yellow, snow, 2*694.5).
%bird_type_impact(yellow, tnt, 1.0).
%bird_type_impact(yellow, pork, 1.0).

bird_type_impact(blue, wood, 3*723.5). % 1808.64 (723.456 2893.824 434.0736 120.58203)
bird_type_impact(blue, ice, 3*2893.8).
bird_type_impact(blue, snow, 3*434.1).
bird_type_impact(blue, stone, 3*120.6).
%bird_type_impact(blue, tnt, 5).
%bird_type_impact(blue, pork, 10).

bird_type_impact(black, wood, 3014.4). % * 7536 (3014.4001 3768.0 678.24005 1507.2001)
bird_type_impact(black, ice, 3768.0).
bird_type_impact(black, snow, 678.2).
bird_type_impact(black, stone, 1507.2).
%bird_type_impact(black, tnt, 5).
%bird_type_impact(black, pork, 10).

bird_type_impact(white, wood, 2717.0). % * 8490.56 (2716.979 3396.2239 611.32025 566.0656)
bird_type_impact(white, ice, 3396.2).
bird_type_impact(white, snow, 611.3).
bird_type_impact(white, stone, 566.1).
%bird_type_impact(white, tnt, 5).
%bird_type_impact(white, pork, 10).

bird_type_impact(_, hill, 0.001).
bird_type_impact(_, pork, 500000).
bird_type_impact(_, _, 2.0).

impact(Bird, Object, Impact) :-
    hasColor(Bird, C),
    hasMaterial(Object, M, _, _, _, _),
    bird_type_impact(C, M, Impact),
    !.

% Domino Impact:

dominoImpact(Bird, _, 9.5) :-
    redbird(Bird).
dominoImpact(Bird, ice, 3) :-
    yellowbird(Bird).
dominoImpact(Bird, wood, 2) :-
    yellowbird(Bird).
dominoImpact(Bird, stone, 1) :-
    yellowbird(Bird).
dominoImpact(Bird, ice, 2) :-
    bluebird(Bird).
dominoImpact(Bird, wood, 8) :-
    bluebird(Bird).
dominoImpact(Bird, stone, 8) :-
    bluebird(Bird).

hasDominoImpact(Bird, Object, P) :-
    hasMaterial(Object, M, _, _, W, H),
    (H > W, W<26 -> dominoImpact(Bird, M, P) ; P is 1),
    !.

%%
%% max_damage(+Bird, +Target, -NewTarget, -Angle, -Extra) tunes a shot at Target to maximum damage,
%% while still somehow hitting Target. Extra lists the objects additionally destroyed
%%

deep_shot(Bird, Target, Angle, NewTarget, Damaged, Depth, NewAngle) :-
    hasMaterial(Target, _, TX, _, _, _),
    hasMaterial(NewTarget, _, OX, _, _, _),
    OX > TX,
    shot_obstacles(NewTarget, Damaged, NewAngle),
    abs(NewAngle-Angle) < 0.5236, % 30 deg. deviation
    member(Target, Damaged),
    penetration(Bird, Damaged, E),
    E < 1.0,
    length(Damaged, Depth).

select_max_shot([T,E,D,A], [_,_,D2,_], [T,E,D,A]) :-
    D>D2, !.

select_max_shot([_,_,D,_], [T2,E2,D2,A2], [T2,E2,D2,A2]) :-
    D=<D2, !.

max_damage(Bird, Target, Angle, NewTarget, NewAngle, Extra) :-
    findall([NT,NTDA, NTD,NTA], deep_shot(Bird, Target, Angle, NT, NTDA, NTD, NTA), DST),
    foldl(select_max_shot, DST, [none,[],0,0], Shot),
    Shot=[NewTarget,Extra,_,NewAngle],
    NewTarget\=none.

%%


%% Values for Energy-calculation are mapped from game/slingshot/cors/fowl/json/Materials.json to our scale.

box_compare(C, Obj1, Obj2) :-
    hasMaterial(Obj1,_,X1,_,_,_),
    hasMaterial(Obj2,_,X2,_,_,_),
    compare(C,X1,X2).

point_line_rel(PX, PY, XS, YS, XE, YE, R) :-
    S is (PX-XS)*(-YE+YS) + (PY-YS)*(XE-XS),
    (S>0 -> R=l; R=r).

% succeeds if some points are left and some are right of line
%crosses(_, _, _, _, _, true, true).
%crosses(XS, YS, XE, YE, [[PX,PY]|PS], true, R) :-
%    point_line_rel(PX, PY, XS, YS, XE, YE, left),
%    crosses(XS, YS, XE, PS, true, R).

%crosses(XS, YS, XE, YE, [[PX,PY]|PS], L, true) :-
%    point_line_rel(PX, PY, XS, YS, XE, YE, right),
%    crosses(XS, YS, XE, PS, L, true).

% secceeds if object intersects line segment
%object_on_line(Obj, XStart, YStart, XEnd, YEnd) :-
%    (hasMaterial(Obj,_,X,Y,W,H) ; hill(Obj, X,Y,W,H)),
%    ((XStart =< X+W, X =< XEnd) ; (YStart =< Y+H, Y =< YEnd)). % bounding boxes intersect
%    crosses(XStart, YStart, XEnd, YEnd, [[PX,PY],[PX+W,PY], [PX+W,PY+H], [PX,PY+H]], false, false)%.

% succeeds if line segments [X1S, Y1S] -> [X1E,X1E] and [X2S, Y2S] -> [X2E, Y2E] intersect,
% IX, IY are unified with intersection point
% formula from https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
lines_intersect(X1S,Y1S,X1E,Y1E,X2S,Y2S,X2E,Y2E, IX, IY) :-
    S1_X is X1E - X1S,
    S1_Y is Y1E - Y1S,
    S2_X is X2E - X2S,
    S2_Y is Y2E - Y2S,
    DIV1 is (-S2_X * S1_Y + S1_X * S2_Y),
    DIV2 is (-S2_X * S1_Y + S1_X * S2_Y),
%    format('DIV1=~w~nDIV2=~w~nsegments=~w  and ~w~n~n', [DIV1, DIV2, [X1S,Y1S,X1E,Y1E], [X2S,Y2S,X2E,Y2E]]),
    abs(DIV1) >= 0.00001,
    abs(DIV2) >= 0.00001,
     S is (-S1_Y * (X1S - X2S) + S1_X * (Y1S - Y2S)) / DIV1,
    S >= 0,
    S =< 1,
    T is ( S2_X * (Y1S - Y2S) - S2_Y * (X1S - X2S)) / DIV2,
    T >= 0,
    T =< 1,
    IX is X1S + T*S1_X,
    IY is Y1S + T*S1_Y.

%% test line segment intersection on boundary, passes first point as 2nd argument
%% to allow loop-closing
line_boundary_intersect(X1S,Y1S,X1E,Y1E, [X0,Y0], [[XN, YN]], IX, IY) :-
    lines_intersect(X1S,Y1S,X1E,Y1E, XN,YN, X0, Y0, IX, IY).
line_boundary_intersects(X1S,Y1S,X1E,Y1E, _, [[X0, Y0], [X1, Y1] | _], IX, IY) :-
    lines_intersect(X1S,Y1S,X1E,Y1E, X0, Y0, X1, Y1, IX, IY).
line_boundary_intersects(X1S,Y1S,X1E,Y1E, LastPoint, [_ | PRest], IX, IY) :-
    line_boundary_intersects(X1S,Y1S,X1E,Y1E, LastPoint, PRest, IX, IY).

%% convenience predicate to check line segment to polygon (= list of points)
%% intersection
line_poly_intersection(X1S,Y1S,X1E,Y1E, [P1 | Prest], IX, IY) :-
    line_boundary_intersects(X1S,Y1S,X1E,Y1E, P1, [P1 | Prest], IX, IY).


%% check intersection of parabola and polygon
line_parabola_intersection([X1,Y1], [X2,Y2], X0, Y0, DXMAX, A, B, X1) :-
    abs(X1-X2) < 3, % OK for nearly vertical and much faster than precise check
    X1 =< DXMAX+X0,
    !,
    YP is Y0 - A*(X1-X0)^2 - B*(X1-X0),
    %format('vertical check [~w,~w], [~w,~w] ... YP=~w~n', [X1,Y1,X2,Y2,YP]),
    YP < max(Y1,Y2),
    YP > min(Y1,Y2).

line_parabola_intersection([X1,Y1], [X2,Y2], X0, Y0, DXMAX, A, B, HX) :-
    abs(X1-X2) > 2,  % \= 0 is important
    abs(A)>1e-10,
    !,
    M is (Y2-Y1)/(X2-X1),
    P is (2*A*X0 - B - M)/ (-A),
    Q is (Y0-A*X0*X0+B*X0-Y1+M*X1)/ (-A),
    ROOTTERM is 0.25*P^2 - Q,
    ROOTTERM >= 0,
    IX1 is (-0.5 * P) - sqrt(ROOTTERM),
    IX2 is (-0.5 * P) + sqrt(ROOTTERM),
    !,
    member(HX, [IX1,IX2]),
    HX =< DXMAX+X0,
    HX >= min(X1,X2),
    HX =< max(X1,X2).


poly_parabola_intersection(P0, [PN], X0, Y0, DXMAX, A, B, HX) :-
    line_parabola_intersection(P0, PN, X0, Y0, DXMAX, A, B, HX), !.

poly_parabola_intersection(_, [P1, P2 | _], X0, Y0, DXMAX, A, B, HX) :-
    line_parabola_intersection(P1, P2, X0, Y0, DXMAX, A, B, HX),!.

poly_parabola_intersection(P0, [_, P2 | PREST], X0, Y0, DXMAX, A, B, HX) :-
    poly_parabola_intersection(P0, [P2 | PREST], X0, Y0, DXMAX, A, B, HX).


%%
%% true shape intersection test shape/parabola
%%
%%

%% rotates by angle, then shifts to CX,CY
rot_shift(_Angle, _CX, _CY, [], []).

rot_shift(Angle, CX, CY, [[X,Y] | PS], [[XRS, YRS] | PRS]) :-
    XR is X*cos(Angle) - Y*sin(Angle),
    YR is X*sin(Angle) + Y*cos(Angle),
    XRS is XR+CX,
    YRS is YR+CY,
    rot_shift(Angle, CX, CY, PS, PRS).

parabola_crosses_shape(rect, CX, CY, [W,H,Angle], X0, Y0, DXMAX, A, B, HITX) :-
    %% width (W) is in Y direction @ ANGLE=0
    %% length (H) is in X direction @ ANGLE=0
    %% NB: rotation is clock-wise!
    %% X = x*cos(θ) - y*sin(θ)
    %% Y = x*sin(θ) + y*cos(θ)
    XR is (0.5*H),
    YR is (0.5*W),
    rot_shift(-Angle, CX, CY, [[-XR,-YR], [-XR,YR], [XR,YR], [XR,-YR]], POINTS),
    POINTS = [P1 | _],
    poly_parabola_intersection(P1, POINTS, X0, Y0, DXMAX, A, B, HITX).

parabola_crosses_shape(ball, CX, CY, [R], X0, Y0, _, A, B, HX) :- % FIXME: add true shape test
    YP is Y0 - A*(CX-X0)^2 - B*(CX-X0),
    abs(YP-CY) =< R,
    HX is CX. % FIXME: compute correct point of intersection

parabola_crosses_shape(poly, _, _, [_ | [P1 | POINTS]], X0, Y0, DXMAX, A, B, HX) :-
    poly_parabola_intersection(P1, [P1 | POINTS], X0, Y0, DXMAX, A, B, HX).

parabola_crosses_shape(unknown, CX, _, _, _, _, _, _, _, CX). 

object_on_parabola(Obj, X0, Y0, DXMAX, A, B, HITX) :-
    (hasMaterial(Obj,_,X, _Y, W, _H) ;  % X,Y ist Ecke links oben; +W, +H rechts unten
     hill(Obj, X, _Y, W, _H) ),
    DX is X - X0,
    (X+W)-X0 > 0,
    DX < DXMAX, %% object not behind target

    % Uhoh: the following test only compares bounding box of object to Y coordinates of the parabola
    % on the left and at the right side of the box. This ignores the possibility that the parabola
    % has a climax right in the middle.
    % FIXME: we need to gate  the test such that the parabola has the sae slope on the left and on the
    % right side of the box. For time being we leave the test commented out, so computation is correct
    % at the cost of doing some line/parabola intersections that could have been avoided.
    %
    %PY is Y0 - A*DX*DX - B*DX, % parabola at left end of box
    %DX_BACK is min(DXMAX, X + W - X0),
    %PY_BACK is Y0 - A*DX_BACK*DX_BACK - B*DX_BACK, % parabola at right end of box
    %writeln(['o_o_p', Obj,X,Y,W,H,[DX,PY],[DX_BACK,PY_BACK]]),
    %YL is Y+H,
    %( (Y < PY, PY < YL) ; (PY < Y, PY_BACK > Y) ; (PY < Y, PY_BACK > YL) ; (PY > YL, PY_BACK < Y) ),
    shape(Obj, ShapeType, CX, CY, _, ShapeData),
    %writeln(['p_c_s', ShapeType, CX, CY, ShapeData, X0, Y0, DXMAX, A, B]),
    parabola_crosses_shape(ShapeType, CX, CY, ShapeData, X0, Y0, DXMAX, A, B, HITX).

sort_by_hit_x(REL, [_,X1,_], [_,X2,_]) :-
    compare(REL, X1, X2).

shot_obstacles_and_hit(Target, Objects_Hits, Angle) :-
    slingshotPivot(X0,Y0),
    parabola(Target, Angle, A, B),
    hasMaterial(Target,_,TX,_,_,_), %% <--- FIXME: DXMAX muss anhand des Treffers auf Target bestimmt werden!
    DXMAX is TX - X0, % +(0.5*W)
    findall([O,HX,HY],
	    (
		object_on_parabola(O, X0, Y0, DXMAX, A, B, HX),
		O \== Target,
		HY is (Y0 - A*(HX-X0)^2 - B*(HX-X0))
	    ),
    	    OH),
 %   ((bagof( [O, HX, HY],
%	    ( object_on_parabola(O, X0, Y0, DXMAX, A, B, HX),
%	      O \== Target,
%	      HY is (Y0 - A*(HX-X0)^2 - B*(HX-X0))
%	    ),
%	    OH),!)
%    ; OH=[]),
    predsort(sort_by_hit_x, OH, Objects_Hits).

remove_hit_point([O,_,_], OS, [O|OS]).

shot_obstacles(Target, Objects, Angle) :-
    slingshotPivot(X0,Y0),
    parabola(Target, Angle, A, B),
    hasMaterial(Target,_,TX,_,_,_),
    DXMAX is TX - X0, % +(0.5*W)
    findall([O,HX,HX], % dummy HX
	    (
		object_on_parabola(O, X0, Y0, DXMAX, A, B, _),
		O \== Target
	    ),
	    OH),
    predsort(sort_by_hit_x, OH, Objects_Hits),
    foldl(remove_hit_point, Objects_Hits, [], Objects).


shortest_list([],Shortest,_, Shortest).
shortest_list([(List, Len) | Rest], _, SLen, A) :-
    Len < SLen,
    shortest_list(Rest, List, Len, A).
shortest_list([(_, Len) | Rest], Shortest, SLen, A) :-
    Len >= SLen,
    shortest_list(Rest, Shortest, SLen, A).

fewest_shot_obstacles(Target, Objects) :-
    findall((O,L), (shot_obstacles(Target, O,_), length(O,L)) , [(O1,L1)|Rest]),
    shortest_list(Rest, O1, L1, Objects).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%
%%% computing shots
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% constants for *new* vision module
low_angle_change([ -0.0230, -7.871e-4, 0.0540]).
low_angle_velocity([0.0473, -0.1756,   2.8654]).

high_angle_begin(blue, 1.347847968145141). % 77.226 degrees
high_angle_begin(red, 1.2998514137152968). % 74.476
high_angle_begin(yellow, 1.3095554443563853).
high_angle_begin(black, 1.2701982697239131).
high_angle_begin(white, 1.2106476356458666).

high_angle_change(blue, [-6.2164, 17.7277, -12.5889]).
high_angle_change(red,  [-6.8544, 19.1149, -13.2502]).
high_angle_change(yellow, [-7.1737, 20.0922, -13.9949]).
high_angle_change(black, [-10.4124, 28.4201, -19.2827]).
high_angle_change(white, [-11.8720, 31.2441, -20.4036]).

high_angle_velocity(blue, [39.1345, -119.2619, 92.3808]).
high_angle_velocity(red, [42.1667, -124.9211, 93.8631]).
high_angle_velocity(yellow, [43.7502, -130.3646, 98.4179]).
high_angle_velocity(black,  [65.4336, -186.8649, 134.515]).
high_angle_velocity(white, [73.2264, -199.8274, 137.3380]).

%% computes A*X^2 + B*X + C
quadric(X, [A, B, C], Y) :-
    Y is A*X^2 + B*X + C.

%% computes velocity Vel for bird of color BC launched at Angle
%% ShotHelper angleToVelocity()
launch_velocity(BC, Angle, Vel) :-
    high_angle_begin(BC, AHigh),
    (AHigh =< Angle ->
	 high_angle_velocity(BC, PARAMS)
    ;
    low_angle_velocity(PARAMS)
    ),
    quadric(Angle, PARAMS, V),
    scene_scale(_,S),
    Vel is S*V.

%% computes angles for highh and low shot (ParabolaMath targetToAngles())
target_angles(Vel, TX, TY, A1, A2) :-
    V2 is Vel*Vel,
    ROOTTERM is (V2*V2 - TX*TX - 2*TY*V2),
    ROOTTERM > 0,
    ROOT is (sqrt(ROOTTERM)),
    A1 is atan((V2 - ROOT)/TX),
    A2 is atan((V2 + ROOT)/TX).

%% iterates velocity<->angle estimates I times
%% correct_estimate(bird color, target x, target y, approx. angle, resulting angle, resulting velocity, loop count)
correct_estimate(BC, _, _, A, A, Vel, _, 0) :-
    launch_velocity(BC, A, Vel), !.

correct_estimate(BC, TX, TY, A, CA, Vel, Upper, I) :-
    I>0, !,
%    format('A=~w, CA=~w, Vel=~w, Upper=~w, I=~w~n', [A, CA, Vel, Upper, I]),
    launch_velocity(BC, A, V),
    target_angles(V, TX, TY, CA1, CA2), % angles for upper and lower, select right one
    NI is I-1,
    (Upper ->
	 correct_estimate(BC, TX, TY, CA1, CA, Vel, Upper, NI)
    ;
    correct_estimate(BC, TX, TY, CA2, CA, Vel, Upper, NI)).

%% computes error as Euclidean difference to goal using high_shot velocity estimates
error_high_estimate(BC, TRX, TRY, ANGLE, ERROR) :-
    high_angle_velocity(BC, PARAMS),
    quadric(ANGLE, PARAMS, V),
    scene_scale(_,S),
    Vel is S*V,
    V1 is cos(ANGLE)*Vel,
    V2 is sin(ANGLE)*Vel,
    A is (-0.5/(V1^2)),
    V1 \= 0,
    B is (V2 / V1),
    ERROR is abs(TRY - A*TRX^2 - B*TRX).

%% binary search for high shot closest to target TRX, TRY
correct_estimate_high_shot(_, _, _, ANGLE, LOWER, UPPER) :-
    abs(UPPER - LOWER) < 1e-4,
    ANGLE is UPPER,
    !.
correct_estimate_high_shot(BC, TRX, TRY, ANGLE, LOWER, UPPER) :-
    abs(UPPER - LOWER) >= 1e-4,
    MID is (0.5*(UPPER+LOWER)),
    MID_PLUS is (MID + 1e-5),
    MID_MINUS is (MID - 1e-5),
    error_high_estimate(BC, TRX, TRY, MID_PLUS , ERR_PLUS ),
    error_high_estimate(BC, TRX, TRY, MID_MINUS, ERR_MINUS),
    (ERR_PLUS > ERR_MINUS ->
	 correct_estimate_high_shot(BC, TRX, TRY, ANGLE, LOWER, MID)
    ;
    correct_estimate_high_shot(BC, TRX, TRY, ANGLE, MID, UPPER)).

predict_launch_params(BC, TX, TY, [[CA1, V1], [CA2, V2]]) :-
    slingshotPivot(X0, Y0),
    scene_scale(S,_),
    TRX is ((TX-X0)/S), % relative target points
    TRY is ((Y0-TY)/S),
%    format('target (relative) = [~w,~w]~n', [TRX, TRY]),
    launch_velocity(BC, 0.6981317007977318, V),   % estimate start params for 40 deg.
    target_angles(V, TRX, TRY, A1, A2),
    high_angle_begin(BC, HA),
    %% compute shot1: angle CA1, velocity V1
    (A1 >= HA ->
	 (correct_estimate_high_shot(BC, TRX, TRY, CA1, HA, 1.501),
	 launch_velocity(BC, CA1, V1))
    ;
    correct_estimate(BC, TRX, TRY, A1, CA1, V1, true, 5)),
    %% compute shot2: angle CA2, velocity V1
    (A2 >= HA ->
	 (correct_estimate_high_shot(BC, TRX, TRY, CA2, HA, 1.501),
	  launch_velocity(BC, CA2, V2))
    ;
    correct_estimate(BC, TRX, TRY, A2, CA2, V2, false, 5)).

%% ParabolaMath velocityComponentsToParabola()
%% NB: call from high_angle error function relying on scale=1 does *not* use this predicate
velocity_components_to_parabola(V1, V2, A, B) :-
    scene_scale(S,_),
    A is (-0.5/(S*V1^2)),
    V1 \= 0,
    B is (V2 / V1).

%% ShotPlanner parabolaForActualAngle()
parabola_for_actual_angle(BC, Angle, A, B) :-
    launch_velocity(BC, Angle, Vel),
    V1 is cos(Angle)*Vel,
    V2 is sin(Angle)*Vel,
    velocity_components_to_parabola(V1, V2, A, B).

angle_to_release_point(BC, Angle, RX, RY) :-
    high_angle_begin(BC, HA), % launch_to_actual()
    (Angle >= HA ->
	 (high_angle_change(BC, Params), quadric(Angle, Params, Offset))
    ;
    (low_angle_change(Params), quadric(Angle, Params, Offset))),
    Corrected is (Angle+Offset),
%    format('Angle ~w --> ~w~n', [Angle, Corrected]),
    RX is round(-1000 * cos(Corrected)),
    RY is round(+1000 * sin(Corrected)).

% computes total time of flight (TOF) based on velocity (V), angle (A),
% distance to travel along X axis (DX)
time_of_flight(V, A, DX, TOF) :-
    scene_scale(S,_),
    TOF is (815 * (DX/S) / (V*cos(A))). % magic 815

shot_obstacles(A, B, DXMAX, Obstacles) :-
    slingshotPivot(X0, Y0),
    findall([O,HX,HX],
	    (
		object_on_parabola(O, X0, Y0, DXMAX, A, B, HX)
	    ),
	    OH),
    predsort(sort_by_hit_x, OH, Obstacles).

%% returns list of shots (typically 2: high and low)
%% shot: [Target_X, Target_Y, release angle, A, B, list of obstacles on parabola
%%        Time of flight, release point x, release point y]
shots_at_point(Bird, TX, TY, SHOTS) :-
    hasColor(Bird, BC),
    predict_launch_params(BC, TX, TY, AngleVels),
    slingshotPivot(X0, _),
    DXMAX is (TX-X0),
    !,
    findall([TX,TY,Angle, A, B,Obstacles,TOF, RX, RY],
	    (
		member([Angle,V], AngleVels),
		parabola_for_actual_angle(BC, Angle, A, B),
		shot_obstacles(A, B, DXMAX, Obstacles),
		time_of_flight(V, Angle, DXMAX, TOF),
		angle_to_release_point(BC, Angle, RX, RY)
	    ),
	    SHOTS).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%
%%% debugging aids
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% trim_name/2
%% trims atom name for export so it fits into small boxes
%% A : atom such as wood23
%% N : resulting name, e.g. "w23"

drop_alphas([],[]).
drop_alphas([H|R], [H|R]) :-
    char_type(H, digit).
drop_alphas([_|R], D) :-
    drop_alphas(R, D).

trim_name(Atom, Name) :-
    atom_string(Atom, Str),
    string_chars(Str, [C | Chrs]),
    drop_alphas(Chrs, Clean), !,
    string_chars(Name, [C | Clean]).

%% writes TIKZ drawing commands
%% Out    : stream to write to
%% ID     : label of the object to add, e.g., wood2
%% Color  : fill color
%% Points : list of points
export_poly(Out,ID,Color,Points,CX,CY,A) :-
    format(Out, '\\draw[fill=~a] ', [Color]),
    forall(member([X,Y], Points), format(Out, '(~f,~f) -- ', [0.05*X,-0.05*Y])),
    trim_name(ID, Label),
    format(Out, 'cycle;~n\\node[rotate=~f] at (~f,~f) {\\small ~w};~n', [180.0*(A / pi), 0.05*CX, -0.05*CY, Label]).

%% exports a specific type of shape
export_shape(Out, ID, rect, X, Y, [W, H, A]) :-
    hasMaterial(ID, M, _, _, _, _),
    %% draw object
    XRa is (0.5*H),
    YRa is (0.5*W),
    rot_shift(-A, X, Y, [[-XRa,-YRa], [-XRa,YRa], [XRa,YRa], [XRa,-YRa]], Points),
    export_poly(Out,ID,M,Points,X,Y,A).

export_shape(Out, ID, unknown, X, Y, _) :-
    hasMaterial(ID, M, _, _, _, _),
    trim_name(ID, Label),
    format(Out, '\\draw[fill=~a] (~f,~f) circle (8pt) node {\\small ~a};~n', [M, X*0.05, -0.05*Y, Label]).

export_shape(Out, ID, poly, X, Y, [_ | Points]) :-
    (hasMaterial(ID, M, _, _, _, _) ; M=lightgray), % hills are of shape type poly but don't have a material assigned
    export_poly(Out,ID,M,Points,X,Y,0).

export_shape(Out, ID, ball, X, Y, [R]) :-
    (hasMaterial(ID, M, _, _, _, _) ; hasColor(ID,M)), % birds are of shape type ball but don't have a material assigned; use red instead
    format(Out,'\\draw[draw,fill=~a] (~f, ~f) circle (~f) node {~w};~n', [M, 0.05*X, -0.05*Y, 0.05*R, ID]).

draw_parabola(_Out, X, HITX, _A, _B, SX, _SY) :- 
    (X + SX) > HITX, !.

draw_parabola(Out, X, HITX, A, B, SX, SY) :-
    (X + SX) =< HITX,
    format(Out, '-- (~f, ~f)', [0.05*(SX+X), -0.05*(SY-A*X*X-B*X)]),
    ((X+20+SX > HITX, HITX-SX-X > 2) -> NX is (HITX-SX-0.5) ; NX is X+20),
    draw_parabola(Out, NX, HITX, A, B, SX, SY).


export_parabola(Out, A, B, Target) :-
    slingshotPivot(SX, SY),
    shape(Target, ShapeType, TX, TY, _, ShapeData),
    (parabola_crosses_shape(ShapeType, TX, TY, ShapeData, SX, SY, 1000, A, B, HITX) ->
	 (format(Out, '\\draw[dotted] (~f,~f)', [0.05*SX, -0.05*SY]),
	  draw_parabola(Out, 10, HITX, A, B, SX, SY),
	  writeln(Out, ';'))
    ; true).
    
export_plan(Out, [Target, Angle, _Strategy, _Confidence, _Pigs]) :-
%    shape(Target, _, TX, TY, _, _),
%    RA is ((pi*Angle)/180.0),
%    TXScaled is (TX*0.05),
%    TYScaled is (TY*(-0.05)),		     
%    SX is (TXScaled - 5*cos(RA)),
%    SY is (TYScaled - 5*sin(RA)),
%    EX is (TXScaled - 0.2*cos(RA)),
%    EY is (TYScaled - 0.2*sin(RA)),
    (parabola(Target, Angle, A, B) -> export_parabola(Out, A, B, Target) ; true).
%    format(Out, '\\draw[dashed,->] (~f,~f) -- (~f,~f);~n', [SX, SY, EX, EY]).

	 
export_plan(Out, [Target, Angle, Strategy, Confidence]) :-
    export_plan(Out, [Target, Angle, Strategy, Confidence, []]).

describe_plan(Out, [Target, Angle, Strategy, Confidence, Pigs]) :-
    format(Out,'~w & ~w & ~w & ~2f & ~w\\\\', [Target, Angle, Strategy, Confidence, Pigs]).

describe_plan(Out, [Target, Angle, Strategy, Confidence]) :-
    describe_plan(Out, [Target, Angle, Strategy, Confidence, []]).

table_of_plans(Out, Plans) :-
    writeln(Out, '\\begin{tabular}{lllll}'),
    writeln(Out, 'target & angle & strategy & confidence & destroys\\\\ \\hline'),
    forall(member(P, Plans), describe_plan(Out, P)),
    writeln(Out, '\\end{tabular}').


%%
%% Writes a latex file displaying the current scene, i.e., all objects mentioned as shape/6 predicates.
%% Also indicates where shots are planned according to list of Plans in the format
%% [[target, angle, strategy, confidence, pigs_affected] | ... ]
%%
export_tikz(Plans) :-
    %% open file, write latex header
    open('scene.tex', write, Out),
    writeln(Out, '\\documentclass{standalone}'),
    writeln(Out, '\\usepackage{tikz}'),
    writeln(Out, '\\definecolor{ice}{rgb}{0.6,0.7,1.0}'),
    writeln(Out, '\\definecolor{stone}{rgb}{0.5,0.5,0.5}'),
    writeln(Out, '\\definecolor{wood}{rgb}{0.9,0.6,0.1}'),
    writeln(Out, '\\definecolor{pork}{rgb}{0.1,1.0,0.1}'),
    writeln(Out, '\\definecolor{tnt}{rgb}{0.9,0.9,0.0}'),
    writeln(Out, '\\begin{document}'),
    writeln(Out, '\\begin{tikzpicture}'),

    %% draw all objects in scene by  executing goal export_shape/6 defined above for all shapes
    forall(shape(ID,Type,X,Y,_Area,Params), export_shape(Out,ID,Type,X,Y,Params)),

    %% draw slingshot
    slingshotPivot(SX,SY),
    format(Out, '\\draw (~f,~f) -- +(0:1cm) -- +(180:1cm) -- +(0:0) -- +(90:1cm) -- +(270:1cm);~n', [0.05*SX, -0.05*SY]),

    %% draw plans
    forall(member(P, Plans), export_plan(Out, P)),

    %%  finish picture
    writeln(Out, '\\end{tikzpicture}'),

    %% add table of plans
    (Plans\=[] -> table_of_plans(Out, Plans);true),
    
    %% finish document, close file, and typeset
    writeln(Out, '\\end{document}'),
    close(Out),
    shell('pdflatex scene.tex'),
    shell('open scene.pdf').  %  <-- use xdg-open for linux

export_tikz :-
    export_tikz([]).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%
%%% strategy
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

all_hittable([]).
all_hittable([T|Ts]) :-
    isHittable(T,_), !,
    all_hittable(Ts).

flachschuss(Target, Angle) :-
    %    findall(A, isHittable(Target, A), As),
    findall(A, shot_obstacles(Target,[], A), As),
    max_list(As, Angle).

steilschuss(Target, Angle) :-
    findall(A, isHittable(Target, A), As),
    min_list(As, Angle).

linksschwein(P, [], P).
linksschwein(P, [P2|Pigs], Target) :-
    pig(P, PX, _, _, _),
    pig(P2,P2X,_,_,_),
    (PX<P2X -> linksschwein(P,Pigs,Target) ; linksschwein(P2,Pigs,Target)).

topschwein(P, [], P).
topschwein(P, [P2|Pigs], Target) :-
    pig(P, _, PY, _, _),
    pig(P2,_,P2Y,_,_),
    (PY>P2Y -> topschwein(P,Pigs,Target) ; topschwein(P2,Pigs,Target)).


% select pig from an all-hittable set of pigs by choosing shot
% with chance of side-effects on other pigs
preferred_shot(_, [P|Pigs], Target, Angle, C) :-
    bounding_box_lst(Pigs, XMin, YMin, XMax, YMax),
    ( ((YMax - YMin) > 2*(XMax - XMin)) -> (linksschwein(P,Pigs,Best), flachschuss(Best,BestAngle)),
					   (topschwein(P,Pigs,Best), steilschuss(Best,BestAngle))),
    !,
    member(Target, [P|Pigs]),
    (Target == Best -> (Angle is BestAngle, C is 1.0) ; (isHittable(Target, Angle), C is 0.9)).

penetration(_, [], 0).
penetration(Bird, [O|OS], E) :-
    penetration(Bird, OS, E2),
    shape(O,_,_,_,AREA,_),
    impact(Bird,O,I),
    REL_IMPACT is (AREA*9.3) / I, %% FIXME: * SCALE^2 REALLY?!
    E is E2 + REL_IMPACT.

second_chance(OBJS) :-
    member(O,OBJS),
    (pig(O) ; (findall(O2, isOn(O2,O), ABOVE),second_chance(ABOVE))),
    !.

%%%
%%% white birds' airbombs
%%%

poly_line_intersection([X1,Y1], [[XN,YN]], LX1, LY1, LX2, LY2, HITX, HITY) :-
    lines_intersect(X1,Y1,XN,YN,  LX1, LY1, LX2, LY2, HITX, HITY).

poly_line_intersection(_, [[X1,Y1], [X2,Y2] | _], LX1, LY1, LX2, LY2, HITX, HITY) :-
    lines_intersect(X1,Y1, X2,Y2, LX1, LY1, LX2, LY2, HITX, HITY).

poly_line_intersection(P1, [_| PS],  LX1, LY1, LX2, LY2, HITX, HITY) :-
    poly_line_intersection(P1, PS,  LX1, LY1, LX2, LY2, HITX, HITY).

line_crosses_shape(rect, CX, CY, [W,H,Angle], LX1, LY1, LX2, LY2, HITX, HITY) :-
    %% width (W) is in Y direction @ ANGLE=0
    %% length (H) is in X direction @ ANGLE=0
    %% NB: rotation is clock-wise!
    %% X = x*cos(θ) - y*sin(θ)
    %% Y = x*sin(θ) + y*cos(θ)
    XR is (0.5*H),
    YR is (0.5*W),
    rot_shift(-Angle, CX, CY, [[-XR,-YR], [-XR,YR], [XR,YR], [XR,-YR]], POINTS),
    POINTS = [P1 | _],
%    writeln(POINTS),
    poly_line_intersection(P1, POINTS, LX1, LY1, LX2, LY2, HITX, HITY).

%% from https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
line_crosses_shape(ball, CX, CY, [R], LX1, LY1, LX2, LY2, HITX, HITY) :-
    A is (LX2 - LX1)^2 + (LY2 - LY1)^2,
    B is 2*(LX2 - LX1)*(LX1 - CX) + 2*(LY2-LY1)*(LY1-CY),
    C is (LX1 - CX)^2 + (LY1 - CY)^2 - R^2,
    ROOTTERM is B^2-4*A*C,
    ROOTTERM >= 0,
    T1 is (sqrt(ROOTTERM) - B) / (2*A),
    T2 is (sqrt(ROOTTERM) + B) / (2*A),
    member(T, [T1,T2]),
    T>=0,
    T=<1,
    !,
    HITX is (LX2-LX1)*T + LX1,
    HITY is (LY2-LY1)*T + LY1.

line_crosses_shape(poly, _, _, [_ | [P1 | POINTS]], LX1,LY1,LX2,LY2, HITX, HITY) :-
    poly_line_intersection(P1, [P1 | POINTS], LX1, LY1, LX2, LY2, HITX, HITY).


object_on_vline(O,PX,YUP,YDOWN,HITY) :-
    (hasMaterial(O,_,OXL,OYUP,OW,OH) ; hill(O, OXL,OYUP,OW,OH)),
    OXL<PX,
    OXL+OW > PX,
    ( (YDOWN >= OYUP, YDOWN =< OYUP+OH) ; (YUP >= OYUP, YUP =< OYUP+OH) ; (YUP =< OYUP, YDOWN >= OYUP+OH) ),
%    format('checking ~w further...~n', [O]),
    shape(O, ShapeType, CX, CY, _, ShapeData),
    line_crosses_shape(ShapeType, CX, CY, ShapeData ,PX,YUP,PX,YDOWN, _, HITY).

down_order(=,[O,_],[O,_]).
down_order(<,[_,Y1],[_,Y2]) :- Y1<Y2.
down_order(>,[_,Y1],[_,Y2]) :- Y1>Y2.

pigs_on_drop(PX, YUP, YDOWN, Pigs) :-
    %% all objects on path
    findall([O,HITY], (shape(O,_,_,_,_,_), object_on_vline(O,PX,YUP,YDOWN,HITY)), ObsHits),
    predsort(down_order, ObsHits, Objects),
    !,
    \+((member([H,_], Objects), hill(H))), % no hill inbetween
    ( Objects=[] ->
      findall(P, (pig(P), shape(P,_,CPX,CPY,_,_), sqrt((CPX-PX)^2 + (CPY-YDOWN)^2)<30), Pigs)
    ;
    (Objects=[[_,Y1]|_], findall(P, (pig(P), shape(P,_,CPX,CPY,_,_), sqrt((CPX-PX)^2 + (CPY-Y1)^2)<30), Pigs))).

line_crosses_bb(O, X1, Y1, X2, Y2) :-
    (hasMaterial(O, _, XL, YU, W, H) ; hill(O, XL, YU, W, H)),
    XR is XL+W,
    YD is YU+H,
    POINTS = [[XL,YU], [XL, YD], [XR, YD], [XR, YU]],
    member([PLX, PLY], POINTS),
    point_line_rel(PLX, PLY, X1, Y1, X2, Y2, l),
    member([PRX, PRY], POINTS),
    point_line_rel(PRX, PRY, X1, Y1, X2, Y2, r),
%    format('object ~w further considered (l=[~w,~w], r=[~w,~w])...~n', [O,PLX,PLY,PRX,PRY]),
    !.

white_second_damage(X,Y, CNT) :-
    LX2 is X+Y,
%    writeln([[X,Y], [LX2,0]]),
    findall(O, (shape(O, ST, CX, CY, _, SD), line_crosses_bb(O, X, Y, LX2, 0), line_crosses_shape(ST, CX, CY, SD, X, Y, LX2, 0, _, _)), HITS),
%    writeln(HITS),
    length(HITS, CNT).

bombtarget(Bird, PX, PY, Y, [X0, Y0, RX, RY, TAP], C, Pigs) :-
    Y >= 0,
    slingshotPivot(X0,Y0),
    pigs_on_drop(PX, Y, PY, Pigs),
    !,
    shots_at_point(Bird, PX, Y, SHOTS),
    (
	(member([_,_,_,_,_,[],TAP,RX,RY], SHOTS), !,
	 white_second_damage(PX,Y, CNT),
	 C is 1.0+0.01*CNT)
    ;
    (YABOVE is Y-20, bombtarget(Bird, PX, PY, YABOVE, [X0, Y0, RX, RY, TAP], C, Pigs))
    ).


%% air bombs
airbomb(Bird, Target, 42, ShotDesc, C2, Pigs) :-
    is_goal(Target, Value),
    shape(Target,_,PX,PY,_,_),
    SY is PY-20,
    bombtarget(Bird, PX, PY, SY, [X0,Y0,RX,RY,TAP], C,Pigs),
    C2 is C*Value,
    X0_INT is round(X0),
    Y0_INT is round(Y0),
    TAP_INT is round(TAP*0.95),
    swritef(ShotDesc, '/%w/%w/%w/%w/%w', [X0_INT,Y0_INT,RX,RY,TAP_INT]).

% direct shot at hittable pigs
targetPig(Bird, Target, Angle, C, [Target]) :-
    hasColor(Bird, Color),
    Color\=white,
    findall(P, pig(P), Pigs),
    all_hittable(Pigs),
    findall(B, bird(B), Birds),
    length(Pigs, Num_Pigs),
    length(Birds, Num_Birds),
    Num_Pigs =< Num_Birds,
    preferred_shot(Bird, Pigs, Target, Angle, C).

% direct shot at hittable pig
targetPig(Bird, Target, Angle, Conf, [Target]) :-
    hasColor(Bird,Color),

    %%%% FIXME: erst zu jedem schwein den flachschuss bestimmen, dann
    %%%%        aus der liste mit paaren per member die schuesse ziehen.
    %%%%        Steilschuesse ggf. als 'last resort' generieren

    Color\=white,
    pig(Target),  %leftmost_pig(Target),
    findall(A,isHittable(Target, A), AS),
    max_list(AS, Angle), 
    (num_of_pigs_remaining(1) -> Conf is 1.0 ; Conf is 0.6).

% penetration shot at pig
targetPig(Bird, Target, Angle, Confidence, [Target]) :-
    pig(Target),
    %\+isHittable(Target,_),
    shot_obstacles(Target, Objects, Angle),
%    writeln(Objects),
    penetration(Bird, Objects, P),
    (second_chance(Objects) -> Bonus is 0.2 ; Bonus is 0.0),
    P =< 1.5,
    ((P<1.0) -> Confidence is 1.0+Bonus ; (Confidence is Bonus + 1.0 - 0.33*P)).

/*
penetrate(Bird, Target, Angle, Desc, Confidence, [Target]) :-
    (pig(Target) ; tnt(Target)),
    \+isHittable(Target,_),
    shape(Target, _, X, Y, _, _),
    shots_at_point(B, X, Y, SHOTS),
    member([_,_,_,_,_,Objects,TOF,RX,RY], SHOTS),
    penetration(Bird, Objects, P),
    (second_chance(Objects) -> Bonus is 0.2 ; Bonus is 0.0),
    P =< 1.5,
    ((P<1.0) -> Confidence is 1.0+Bonus ; (Confidence is Bonus + 1.0 - 0.33*P)).
*/


% This strategy aims to collapse a detected structure

max_supporter([], [], 0).
max_supporter([Cand|CS], MS, MScore) :-
    \+isHittable(Cand,_),
    max_supporter(CS,MS,MScore).
max_supporter([Cand|CS], MS, MScore) :-
    isHittable(Cand,_),
    max_supporter(CS, MS2, MScore2),
    aggregate_all(count, isOn(_,Cand), Above), !,
    (Above > MScore2 -> (MS=[Cand], MScore is Above) ;
     (Above==MScore2 -> (MS=[Cand|MS2], MScore is MScore2) ;
      (MS=MS2, MScore is MScore2))).

%max_supporter([Cand|CS], MS, MScore) :-
%    max_supporter(CS, MS2, MScore2),
%    (isHittable(Cand,_) -> (findall(U, isOn(U,Cand), US),
%			    length(US, Cnt),
%			    (Cnt >= MScore2 -> (MScore is Cnt, MS=Cand) ; (MScore is MScore2, MS = MS2)))
%    ; (MScore is MScore2, MS=MS2)).

sum_width([],X,X).
sum_width([O|OS], Accu, S) :-
    hasMaterial(O,_,_,_,W,_),
    Accu2 is Accu + W,
    sum_width(OS,Accu2,S).

loose(Object) :-
    hasMaterial(Object, _, _, _, Width, _),
    findall(O, isOn(O,Object), Above),
    sum_width(Above, 0, AW),
    AW < Width div 4,
    findall(O, isOn(Object,O), Below),
    sum_width(Below, 0, BW),
    BW < Width div 4.


pigs_in_struct(Structure, N, Pigs) :-
%    bagof(P, (pig(P), belongsTo(P, Structure)), Pigs),
    %    length(Pigs,N), !.
    findall(P, (pig(P), belongsTo(P, Structure)), Pigs),
    length(Pigs,N).

%pigs_in_struct(_, 0, []).

critical_effect(_,Target, Criticals, 0.0) :-
    member(Target, Criticals).
critical_effect(Bird,Target, Criticals, -0.2) :-
    member(X, Criticals),
%    aggregate_all(count, isOn(X,_), Supps),
    isOn(X, Target),
    penetration(Bird, [Target], E),
    E < 0.9.

% checks whether a target connects vis isLeft/isRight to a hill
lean_to_hill(Target) :-
    isLeft(Target, X),
    lean_to_hill(X).

lean_to_hill(Target) :-
    \+(isLeft(Target, _)),
    hasMaterial(Target, _, X, Y, W, H),
    PX0 is (X+W-1),
    PX1 is (PX0+6),
    PY is (Y+0.5*H),
    hill(Hill),
    shape(Hill, poly, _, _, _, [ _ | POINTS]),
    line_poly_intersection(PX0,PY,PX1,PY, POINTS, _, _).

sets_overlap(Set1, Set2) :-
    member(O, Set1),
    member(O, Set2), !.

objects_protect_pigs(Objs, Pigs) :-
    findall(P, (pig(P), member(P, Objs)), Pigs),
    Pigs \= [], !.

objects_protect_pigs(Objs, Pigs) :-
    findall(P, (pig(P), shot_obstacles(P, OS, _), sets_overlap(OS,Objs), !), Pigs),
    Pigs \=[], !.

collapseTarget(Bird, Critical, Critical) :-
    hasColor(Bird,black) ; (impact(Bird, Critical, I), I>=1.0) ; loose(Critical).

collapseTarget(Bird, Critical, Target) :-
    isBelow(Object, Critical),  % add stability check
    collapseTarget(Bird, Object, Target).

collapseStructure(Bird, Target, Angle, C, Pigs) :-
    \+(hasColor(Bird,black)),
    structure(Structure),
    pigs_in_struct(Structure, N, Pigs),
    N>0,
    belongsTo(Target, Structure),
    isHittable(Target, _),
    hasOrientation(Target, horizontal),
    \+isLeft(_,Target),
    \+((isOn(Target,X), \+(hill(X) ; hasOrientation(X,vertical)))),
    isOn(Target, XX),
    \+hill(XX),
    \+(lean_to_hill(Target)),
    C is 0.9,
    flachschuss(Target, Angle).

% collapseStructure_(+Birds, -Target, -Confidence)
collapseStructure(Bird, Target, Angle, C, Pigs) :-
    belongsTo(Target, Structure),
%    pigs_in_struct(Structure, N, Pigs),
%    N > 0, % FIXME: besser wahrscheinlichkeit des erlegens der schweine
    findall(O, belongsTo(O,Structure), Objs),
    %    bounding_box_lst(Objs, X0, Y0, X1, Y1),
    objects_protect_pigs(Objs, Pigs),
    max_supporter(Objs, Criticals, S),
    critical_effect(Bird, Target, Criticals, Modifier),
%    member(Target, Criticals),
%    collapseTarget(Bird, Critical, Target),
    findall(A, isHittable(Target,A), AS),
    max_list(AS, Angle),
    \+pig(Target),
    (\+hasMaterial(Target,stone,_,_,_,_) ; hasColor(Bird,black)),
    (((hasMaterial(Target,wood),hasColor(Bird,yellow)) ; (hasMaterial(Target,ice),hasColor(Bird,blue))) -> Bonus is 0.2 ; Bonus is 0.0),
    length(Objs, Num_Of_Objs),
    impact(Bird, Target, I),
%    format('S==~w, Num_Of_Objs=~w, I=~w~n', [S,Num_Of_Objs,I]),
    C is min(1.0,0.6 + 0.1*((S+1)/ Num_Of_Objs) + Bonus + 0.00002*I + Modifier).

% nudge whole structure that rests on a ball
collapseStructure(_, Target, Angle, 0.8, Pigs) :-
    structure(Structure),
    pigs_in_struct(Structure, N, Pigs),
    N>0,
    belongsTo(B,Structure),
    hasForm(B,ball),
    isOn(B,ground),
    isOn(Target, B),
    isHittable(Target, _),
    flachschuss(Target, Angle),
    Angle > -45.

%domino plan, increse confidence with more structures that collapse on another

increseStructuresAffected(StructuresAffected, NewStructuresAffected) :-
    NewStructuresAffected is StructuresAffected + 1.

% collapsingOnOther_(+Structure1, +Structure2, +StructuresAffected, +Energy, -Confidence)
collapsingOnOther(Bird, Target, Structure1, Structure2, StructuresAffected, Energy, C) :-
    %isTower(Structure1),
    collapsesInDirection(Structure1, Structure2, away),
    isTower(Structure2),
	hasDominoImpact(Bird, Target, P),
    increseStructuresAffected(StructuresAffected, NewStructuresAffected),
    collapsingOnOther(Bird, Target, Structure2, _Structure3, NewStructuresAffected, Energy + ((100 - Energy) - (Energy / P)), C),
    !.

collapsingOnOther(_Bird, _Target, _Structure1, _Structure2, StructuresAffected, _Energy, C) :-
    StructuresAffected == 2,
    C is 0.5,
    !.

collapsingOnOther(_Bird, _Target, _Structure1, _Structure2, _StructuresAffected, Energy, C) :-
    C is Energy / 100,
    !.

worth(Struct) :-
    belongsTo(X, Struct),
    is_goal(X,_), !.

% rule to handle single domino: drop object on target
domino(Bird, Target, Angle, C, Pigs) :-
    \+hasColor(Bird, black),
    is_goal(Object, Importance),
    \+isHittable(Object, _),
    hasMaterial(Target, _, X, Y, W, H),
    hasMaterial(Object, _, OX, OY, _, _),
    OY > Y,
    XH is X+H,
    between(X, XH, OX),
    isHittable(Target, Angle),
    between(-50,50, Angle),
    >(H, 1.5*W),
    XLeft is X+W+4,
    XRight is X+W+W+8,
    YDown is max(OY-2, Y+H),
    forall(in_vertical_corridor(O, XLeft, XRight, Y, YDown), is_goal(O,_)),
    (pig(Object) -> Pigs = [Object] ; Pigs = []),
    C is 0.8*Importance.


% domino_(+Bird, -Target, -Confidence)
domino(Bird, Target, Angle, C, []) :-
    object(Target),
    \+pig(Target),
    in_slingshot(Bird),
    isHittable(Target, Angle),
    between(-35,35,Angle),
    belongsTo(Target, Structure1),
    %findall(A,isHittable(Target,A), AS), % flat shot if possible
    %max_list(AS,Angle),
    isCollapsable(Structure2),
    not(Structure1==Structure2),
    ((worth(Structure1) ; worth(Structure2)), !),
    %collapsingOnOther(Bird, Target, Structure1, Structure2, 1, 60, C),
    structure_bounding_box(Structure1, _, S1Y0, S1X1, S1Y1),
    structure_bounding_box(Structure2, S2X0, _, _, S2Y1),
    S1X1 < S2X0,             % s1 starts left of s2
    S1X1+(S1Y1-S1Y0) > S2X0, % s1 can fall on s2
    S2Y1 > S1Y0,             % s2 not above s1
    isTower(Structure1),
    hasMaterial(Target, M, _, Y, _, H),
    YM is Y + H div 2,
    YH is (2*S1Y0 + 1*S1Y1) div 3, % ideal hitpoint
    dominoImpact(Bird, M, I),
    C is 0.5 + 0.2*abs(YM-YH)/(S1Y1-S1Y0) + I*0.02.

% last resort: hit something above left of any pig
domino_last_resort(_, Target, Angle, C, [P]) :-
  isHittable(Target, Angle),
  pig(P,XP,YP,_,_),
  \+isHittable(P,_),
  hasMaterial(Target,_,XT,YT,_,_),
  XT < XP, % left
  YT < YP, % above (positive Y goes down!)
  (between(-35, 35, Angle) -> C is 0.51 ; C is 0.5).


%plan for black birds, work in progress! isHittable not recognized in situations, has to be looked at!

% blackBird_(+Bird, -Target, -Confidence)

pig_score(X, Y, Pig, Killed, S) :-
    shape(Pig, _, CX, CY, _, _),
    D is ((X-CX)^2 + (Y-CY)^2),
    (D<1500 -> Killed=[Pig] ; Killed=[]),
%    writeln(D),
    S is max(0.0, 1.0 - 0.004*sqrt(D)).

pigs_bomb_score(_, _, [], [], 0).

pigs_bomb_score(X,Y, [P|Ps], Killed, S) :-
    pigs_bomb_score(X, Y, Ps, KPs, S1),
    pig_score(X, Y, P, KP, S2),
    append(KP, KPs, Killed),
    S is S1 + S2.

pigs_in_range(X, Y, Score, KilledPigs) :-
    findall(P, pig(P,_,_,_,_), AllPigs),
    pigs_bomb_score(X, Y, AllPigs, KilledPigs, S),
    (KilledPigs=[] -> Score is 0 ; Score is min(1.0,S)).

blackBird(Bird,Target,Angle, Conf, Pigs) :-
	blackbird(Bird),
	object(Target),
	isHittable(Target,_),
	\+hill(Target),
	\+pig(Target),
	%structure(Structure1),
	belongsTo(Target,Structure1),
	collapsesInDirection(Structure1,_Structure2,away),
	pigs_in_struct(Structure1, P, Pigs),
	P>0,
	flachschuss(Target,Angle),
	Conf is min(1.0, 0.7+P).

blackBird(Bird, Target, Angle, Conf, Pigs) :-
	blackbird(Bird),
	object(Target),
	isHittable(Target,_),
	\+hill(Target),
	\+pig(Target),
	structure(Structure),
	structure(Structure2),
	belongsTo(Target,Structure2),
	collapsesInDirection(Structure,Structure2,away),
	collapsesInDirection(Structure2,Structure,towards),
	pigs_in_struct(Structure2, P, Pigs),
	flachschuss(Target,Angle),
	Conf is min(1.0, 0.75+P).

% shoot close to some pig(s) that will be killed by the explosion
blackBird(Bird, Target, Angle, Conf, Pigs) :-
    blackbird(Bird),
    object(Target),
    isHittable(Target, Angle),
    \+hill(Target),
    \+pig(Target),
    shape(Target, _, TX, TY, _, _),
    pigs_in_range(TX, TY, Conf, Pigs).

%% rule to bomb through hills, shooting at the hill
%% NB: special case not handled by previous methods, since
%%     hills are no targets; hence, we shoot directly at the pig
%% FIXME: THIS REALLY SHOULD BE HANDLED BY PENETRATION SHOTS!
blackBird(Bird, Pig, Angle, Conf, Pigs) :-
    blackbird(Bird),
    pig(Pig),
    shot_obstacles_and_hit(Pig, [[_, HX, HY] | _], Angle), % check hitting at hill?!
    pigs_in_range(HX, HY, Conf, Pigs).

% increasePotential_(+Potential, -NewPotential)
increasePotential(Potential, NewPotential) :-
    NewPotential is Potential + 10.

% pigNotConsideredYet_(+AnotherPig, +ListOfPigs)
pigNotConsideredYet(_, []) :-
    true.
pigNotConsideredYet(AnotherPig, [Pig | Pigs]) :-
    AnotherPig \= Pig,
    pigNotConsideredYet(AnotherPig, Pigs).

% calcHeavyObjectC_(+Ball, +ListOfPigs, +Potential, -Confidence)
calcHeavyObjectC(Ball, Pigs, Potential, C, _) :-
    pig(AnotherPig),
    isOver(Ball, AnotherPig),
    pigNotConsideredYet(AnotherPig, Pigs),
    append([AnotherPig], Pigs, NewListOfPigs),
    increasePotential(Potential, NewPotential),
    <(NewPotential, 100),
    !,
    calcHeavyObjectC(Ball, NewListOfPigs, NewPotential, C, _).
calcHeavyObjectC(_Ball, _Target, Potential, C, _) :-
    C is Potential / 100.

% Tries to find a ball that is above pigs and target the object that is most
% likely to support said ball. Potential targets are: the object the ball is
% on, the object that supports the ball or the ball itself.

% heavyObject_(+Bird, -Target, -Confidence)
heavyObject(_, Target, Angle, C, []) :-
    object(Ball),
    hasForm(Ball, ball),
    pig(Pig),
    ((isOver(Ball, Pig) ; (belongsTo(Ball,Struct), worth(Struct))), !),
    isOn(Ball, Target), % Target: Object the ball is on, object is hittable
    \+hill(Target),
    isHittable(Target,Angle),
    calcHeavyObjectC(Ball, [Pig], 65, C, _).

% Reminder: sort-of duplicate deleted.

heavyObject(_, Target, Angle, C, []) :-
    object(Ball),
    hasForm(Ball, ball),
    pig(Pig),
    isOver(Ball, Pig),
    supports(Target, Ball), % Target: Object that supports the ball
    \+hill(Target),
    isHittable(Target, Angle),
    calcHeavyObjectC(Ball, [Pig], 50, C, _).

heavyObject(_, Target, Angle, C, [Pig]) :-
    hasForm(Target, ball),
    isHittable(Target, Angle),
    pig(Pig),
    isOver(Ball, Pig), %% FIXME: add hills and slopes..
    calcHeavyObjectC(Ball, [Pig], 40, C, _).

% WIP / FIXME / TODO : Heavy Object on Slope

heavyObject(_, Ball, Angle, 0.5, []) :-
    hasForm(Ball, ball),
    isHittable(Ball, _),
    flachschuss(Ball, Angle).

heavyObject(_, Target, Angle, C, []) :-
    object(Ball),
    hasForm(Ball, ball),
    isOn(Ball,Hill),
    hill(Hill),
    is_goal(Victim, Importance),
    (Importance > 0.6),
    isOver(Ball, Victim),
    supports(Target, Ball), % Target: Object that supports the ball
    \+hill(Target),
    isHittable(Target, Angle),
    calcHeavyObjectC(Ball, [Victim], 50, C, _).


%nearby_pigs(Target, Pigs) :-
%    hasMaterial(Target, _, X, Y, _, _),
%    findall(P, (pig(P, PX, PY, _, _), sqrt((PX-X)^2 + (PY-Y)^2) < 50.0), Pigs).

% tnt_(+Bird, -Target, -Confidence)
tnt(Bird,Target, Angle, C, Pigs):-
	hasMaterial(Target,tnt,_,_,_,_),
	shot_obstacles(Target, Obstacles, Angle),
	penetration(Bird, Obstacles, PE),
	PE < 0.99,
	findall(P, (pig(P), canExplode(Target, P)), Pigs),
	belongsTo(Target, Struct),
	findall(O, belongsTo(O, Struct), Damaged),
	aggregate_all(count, (member(P, Damaged), pig(P)), PigsDamaged),
	length(Damaged, NObjects),
%	format('target=~w, Pigs=~w, PigsDamaged=~w, objects damaged=~w~n', [Target,Pigs,PigsDamaged,NObjects]),
	((Pigs=[], PigsDamaged==0) -> C is 0.491 ;
					   (Pigs\=[] -> C is 1.0 ;
						     C is min(0.9, 0.5+0.05*NObjects))).

% center of object
%center(XM, YM, X0, Y0, Width, Height) :-
%    XM is X0 + 0.5*Width,
%    YM is Y0 + 0.5*Height.

%direction(X0, Y0, X1, Y1, D) :-
%    A is atan2(Y1-Y0, X1-X0),

bunker(Bird, Target, Angle, C, AllPigs) :-
%    protects(Struct, Pig),
    pig(Pig,PX,PY,_,_),
    \+isHittable(Pig,_),
    structure(Struct),
    %    isAnchorPointFor(Target, Struct),
    belongsTo(Target,Struct),
    isHittable(Target, Angle),
    structure_bounding_box(Struct, X0, Y0, X1, Y1),
    point_contained(PX, PY, X0, Y0, X1, Y1),
    hasMaterial(Target, M, _, _, _, _),
    dominoImpact(Bird, M, I),
    findall(P, (pig(P,PX,PY,_,_), point_contained(PX,PY, X0, Y0, X1, Y1)), AllPigs),
    (between(-30,45,Angle) -> P is 0.0; P is 1.2), % prefer low shots on left half
    (hasOrientation(Target, horizontal), on_groundlike(Target) -> D is 0.4; D is 0.0), % avoid horizontal targets
    (hasOrientation(Target, horizontal), \+on_groundlike(Target) -> D2 is -0.2; D2 is 0.0),
    C is min(1.0, 0.2+(0.05 * I)-P-D-D2).

connects(XL, YL, WL, HL, XR, YR, _, HR) :-
    YML is YL + HL div 2,
    YMR is YR + HR div 2,
    abs(YML-YMR) < max(10, 3*(HL+HR)), % roughly same level
    XR - (XL + WL) < 20.

ice_cluster_center(Target, horizontal, C) :-
    hasMaterial(Target, ice, X, Y, W, H),
    isHittable(Left, _),
    hasMaterial(Left, ice, XL, YL, WL, HL),
    connects(XL, YL, WL, HL, X, Y, W, H),
    isHittable(Right, _),
    hasMaterial(Right, ice, XR, YR, WR, HR),
    connects(X, Y, W, H, XR, YR, WR, HR),
    C is 0.7.

%count_blocking_ice(_, [], 0).
%count_blocking_ice(BS, [[_, OBSTACLES] | POBSTS], C) :-
%    count_blocking_ice(BS, POBSTS, C2),
%    intersection(BS, OBSTACLES, BLOCKS),
%    length(BLOCKS, B),
%    C is B+C2.


target_ice(Target, Angle, BestScore, []) :-
    % find trajectories at pigs that need ice to be removed...
    findall([P,O,A], (pig(P),shot_obstacles(P,O,A)), OBS), !,
    member([P,Obstacles,PAngle], OBS),
    % ...but without hills inbetween
    \+ (member(H, Obstacles), hill(H)),
    member(Target, Obstacles),
    isHittable(Target, Angle),
    Angle < PAngle+10,
    Angle > PAngle-10,
    hasMaterial(Target,ice,_,_,_,_),
    findall(CI, (hasOrientation(Target,HW), ice_cluster_center(Target, HW, CI)), Scores),
    Scores\=[],
    max_list(Scores, BestScore).


% Finds a plan for targetting a Pig, returns a list of a target, the strategy chosen, confidence

% plan_(-DecisionList)
plan(Bird,[Target, Angle, "targetPig", C, Pigs]) :-
    targetPig(Bird, Target, Angle, C, Pigs),
    >(C, 0.49).

plan(Bird,[Target, Angle, "defrost", C, Pigs]) :-
    hasColor(Bird,blue),
    target_ice(Target, Angle, C, Pigs),
    >(C, 0.49).

plan(Bird,[Target, Angle, "collapseStructure", C, Pigs]) :-
    collapseStructure(Bird, Target, Angle, C, Pigs).

/*
plan(Bird,[Target, Angle, "collapseStructure", C, Pigs]) :-
    collapseStructure(Bird, CTarget, CAngle, Conf, Pigs),
    ((max_damage(Bird, CTarget, CAngle, MT, A, EXTRA), length(EXTRA, X))
    -> (Target=MT, Angle=A, C is min(1.0, Conf+0.05*X));
     (Target=CTarget, Angle=CAngle, C is Conf)).
*/
plan(Bird,[Target, Angle, "blackBird", C, Pigs]) :-
    blackBird(Bird, Target, Angle, C, Pigs),
    >(C, 0.49).


plan(Bird,[Target, Angle, "domino", C, Pigs]) :-
    domino(Bird, Target, Angle, C, Pigs),
    >(C, 0.49).

plan(Bird,[Target, Angle, "bunker", C, Pigs]) :-
    bunker(Bird, Target, Angle, C, Pigs),
    >(C,0.49).

plan(Bird,[Target, Angle, ShotDesc, C, Pigs]) :-
    hasColor(Bird,white),
    airbomb(Bird, Target, Angle, ShotDesc, C, Pigs).

plan(Bird,[Target, Angle, "tnt", C, Pigs]) :-
    tnt(Bird, Target, Angle, C, Pigs),
    >(C, 0.49).

plan(Bird, [Target, Angle, "heavyObject", C, Pigs]) :-
    heavyObject(Bird, Target, Angle, C, Pigs),
    >(C, 0.49).

last_resort(Plans) :-
    in_slingshot(Bird),
    % FIXME: must be changed to a fall-off-the-wall-strategy!!    
%    findall([Target,Angle,ShotDesc, C],
%	    airbomb(Bird, Target, Angle, ShotDesc, C,_),
%	    Plans_Closeby),
    findall([Target,Angle,"domino", C],
	    domino_last_resort(Bird, Target, Angle, C, _),
	    Plans).
%    append(Plans_Collapse, Plans_Closeby, Plans).

% predicate for comparing plans, plans with high confidence
% killing many pigs go first
plan_compare(REL, [_,_,_,C1,P1], [_,_,_,C2,P2]) :-
    length(P1,PigKill1),
    length(P2,PigKill2),
    ((C1 + 0.1*PigKill1 =< C2 + 0.1*PigKill2) -> REL = > ; REL = <).
plan_compare(=, [T,A,N,S,P], [T,A,N,S,P]).

strip_pigs([],[]).
strip_pigs([[Target, Angle, Strategy, Confidence, _] | Plans], [[Target, Angle, Strategy, Confidence] | StrippedPlans]) :-
    strip_pigs(Plans,StrippedPlans).

% allPlans_(-ListOfPlans)
allPlans(SortedPlans) :-
    in_slingshot(Bird),
    findall(Plans, plan(Bird,Plans), AllPlans),
    predsort(plan_compare, AllPlans, SPlans), !, % remove duplicates to improve parsing in Java (regular expressions are slow!)
    strip_pigs(SPlans, SortedPlans).

%% check for existence of higher-confidence plan
exists_better_plan([Target, Angle, _, Confidence, Goals], [[Target, Angle, _, Confidence2, Goals2] | _]) :-
    subset(Goals, Goals2),
    Confidence < Confidence2, !.

exists_better_plan(P, [_ | Plans]) :-
    exists_better_plan(P, Plans).

%% drop plans for which a more confident alternative exists
remove_inferior_plans([],_,[]).
remove_inferior_plans([Plan | Plans], AllPlans, RestPlans) :-
    (exists_better_plan(Plan, AllPlans) -> remove_inferior_plans(Plans, AllPlans, RestPlans) ;
     (remove_inferior_plans(Plans, AllPlans, RestPlans2), RestPlans=[Plan|RestPlans2])).


all_bird_plans(Bird, Plans) :-
    findall(P, plan(Bird, P), AllPlansDups),
    sort(AllPlansDups, AllPlans), % remove duplicates
    remove_inferior_plans(AllPlans, AllPlans, Plans).

append_lists([], []).
append_lists([L1 | LR], L) :-
    append_lists(LR, L2),
    append(L1,L2,L).

alternative_plan(Pigs, Confidence, [[_, _, _, C2, P2] | _]) :-
    subset(Pigs, P2),
    C2 >= (Confidence-0.15), !.


alternative_plan(Pigs, Confidence, [_ | OPlans]) :-
	alternative_plan(Pigs, Confidence, OPlans).

%%
%% rate_plans changes confidence of plans according to available alternatives
%% we need to increase confidence in plans within CurrentPlans which are significantly
%% better than alternatives to come (e.g., use a yellow bird to destroy a wooden shelter,
%% avoid forthcoming red birds).

rate_plans(CurrentPlans, [], CurrentPlans).
rate_plans([], _, []).
rate_plans([[Target, Angle, Strategy, Confidence, Pigs] | CurrentPlans], OtherPlans, [[Target, Angle, Strategy, NewConfidence, Pigs] | RatedCurrentPlans ]) :-
    length(Pigs, P),
    ((P==0;alternative_plan(Pigs, Confidence, OtherPlans)) -> NewConfidence is Confidence+P*0.01 ; NewConfidence is Confidence+0.5+P*0.01),
    rate_plans(CurrentPlans, OtherPlans, RatedCurrentPlans).

lookahead_plans(LPlans) :-
    birdOrder(_,1), % more than one bird left
    in_slingshot(Bird),
    all_bird_plans(Bird,Greedy_Plans),
    findall(P, (bird(B), \+in_slingshot(B), (all_bird_plans(B,P))), BirdPlans),
    append_lists(BirdPlans, Other_Plans),
    rate_plans(Greedy_Plans, Other_Plans, Plans),
    predsort(plan_compare, Plans, SPlans), !, % remove duplicates to improve parsing in Java (regular expressions are slow!)
    strip_pigs(SPlans, SortedPlans),
    (SortedPlans\=[] ->
	 LPlans=SortedPlans
    ;
    last_resort(LPlans)).


lookahead_plans(Plans) :-
    \+ birdOrder(_,1), % single bird left
    in_slingshot(B),
    all_bird_plans(B,PS), !,
    predsort(plan_compare, PS, SPlans), !, % remove duplicates to improve parsing in Java (regular expressions are slow!)
    strip_pigs(SPlans, SortedPlans),
    (SortedPlans \= [] -> Plans=SortedPlans ; last_resort(Plans)).


%% Entrance point for Java (SWIConnector class)

shoot_test(PLAN) :-
    pig(P),
    shape(P,_,X,Y,_,_),
    in_slingshot(B),
    shots_at_point(B, X, Y, SHOTS),
    SHOTS = [[_,_,A_RAD,_,_,_,TAP,RX,RY] | _],
    slingshotPivot(X0,Y0),
    X0_INT is round(X0),
    Y0_INT is round(Y0),
    TAP_INT is round(TAP),
    ANGLE is round(180.0*(A_RAD / pi)),
    swritef(STRATEGY, '/%w/%w/%w/%w/%w', [X0_INT,Y0_INT,RX,RY,TAP_INT]),
    PLAN = [P,ANGLE,STRATEGY,1.0].

initiateProlog :-
    read(Filename),
    catch(consult(Filename),writeln('incorrect File Name'),initiateProlog()),
    lookahead_plans(AllPlans),
    % findall(P, shoot_test(P), AllPlans),
    writeln(AllPlans),
    flush_output(),
    halt.

main :-
    initiateProlog.

%% for compatibility
easyMain :-
    initiateProlog.
