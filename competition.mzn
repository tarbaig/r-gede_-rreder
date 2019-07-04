% Use this editor as a MiniZinc scratch book
int : n_work_sheets; % number of work sheets in the problem
int : m_activities; % number of activities in the problem
int : horizon; % maximum scheduling time horizon
int : l_roads;

% it is assumed that activities that belong to the samne sheet are consecutive and that precedence is encoded by order !
array[work_sheets] of int: east; % when to start the sheet earliest
array[work_sheets] of int: last; % when to start latest
%array[work_sheets] of bool: mandratory; % is this work_sheet mandratory
array[work_sheets] of set of int: precedence; % which sheet needs to be done before which sheet, this should be in 
array[work_sheets] of int: duration;
array[activities] of int: activities_to_roads; % mapping form activities to roads
array[roads,days] of int: pertubation_cost ; % how much building on this day hurts; If this can be a funtion in minizinc make it so!
  
array[work_sheets] of int: sheet_to_first_act; % mapping of worksheet to first activitiy
%array[work_sheets] of int: sheet_to_last_act; % mapping of worksheet to last activity
array[activities] of int: act_to_sheet; % mapping of activity to worksheet

set of int: set_sheet_to_first_act = {a|a in sheet_to_first_act};
set of int: work_sheets = 1..n_work_sheets; %index set used to later access the arrays
set of int: activities = 1..m_activities;
set of int: days = 1..horizon;
set of int: roads=1..l_roads;

% we will need these later but initially all sheets are mandratory hence we do not need them now
% array[work_sheets] of var bool: g_k; % is worksheet k executed? This we will branch on
% array[activities] of var bool: f_i; % is activiti i executed

array[work_sheets] of var int: t_w_k; % starting time of the worksheet, this we will branch on too

array[activities] of var int: act_starting_times; % when do the activities start, the first activity of each sheet need to be constraint to be start at the same time as the sheet 
% all need to be constraint to be constarint against each other 

array[activities] of var int: act_ending_times; %when do the activities end, this is populated by constraing
% ending times must be before the horizon

% CONSTRAINTS TO ADD%

% Constrain activities to be active whenever their sheet is active initially all sheet are mandratory hence we do not need that now
% constraint forall(a in activities)(f_i[a]=g_k[act_to_sheet[a]]) 

% constraint first activity of a work sheet to be at the same time as the starting time of the sheet 
constraint forall(s in work_sheets)( act_starting_times[sheet_to_first_act[s]] = t_w_k[s] );

% constarint the starting time of the work sheet to be between the start and the end IFF its  wokr sheets to be activned (reificatio)
constraint forall(s in work_sheets)(t_w_k[s] < last[s]);
constraint forall(s in work_sheets)(east[s] < t_w_k[s]);

% constarint mondratory work sheets to be active
%constraint forall(s in work_sheets) (mandratory[s] -> g_k[s]) % I AM NOT SURE IF THIS IS THE RIGHT WAY TO USE THE IMPLICATION.CHECK THAT

% constraint worksheets to be in the reight order IFF they are active reification
constraint forall(s in work_sheets)(
                  forall(p in precedence[s])
                        (t_w_k[p] + duration[p] <= t_w_k[s]));

%max horizon constraint
constraint max(act_ending_times) <= horizon;

% constraint the maximum number of roads the be blocked at the same time to be 
%ADD LATER 
int: maxBlockedRoads;
array[days, roads] of bool isRoadBlocked;
array[days] of int nblockedRoads;

constraint forall (d in days)(
  nblockedRoads[d] =  sum(j in roads) (isRoadBlocked[d,j]);
)

constraint forall (d in days)(
  nblockedRoads[d] <= maxBlockedRoads;
)



%constarint the work center capacity. The data structures for that are not even active jet
%ADD LATER 

% constraint first activity of a worksheet to be at 0 if it is not activated ? Maybe if reification makes the search slow?

% constarint all activities of a sheet ( those between start and end ) to start after their predecessor ended
constraint forall(s in work_sheets)(
                  forall(a in activities where not (a in set_sheet_to_first_act))
                    (act_starting_times[a]=act_starting_times[a-1]+1)); %this can be improved by adding constraints that reach farther [a]=[a-2]+2 ... an itterator over or by constrining to the offset from the first activity of the sheet? [a]=[first of sheet] + a-first_of_sheet
%
constraint forall(s in work_sheets)(
                  forall(a in activities)
                    (act_ending_times[a]=act_starting_times[a]+1));
% define objective funtion and solve

%var int: obj = max( [pertubation_cost[activities_to_roads[a],act_starting_times[a]] | a in activities]);

solve satisfy;
