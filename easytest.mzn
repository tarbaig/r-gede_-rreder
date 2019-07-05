int : n_work_sheets; % number of work sheets in the problem
int : horizon; % maximum scheduling time horizon
int : l_roads; % number roads

array[work_sheets] of int: east; % when to start the sheet earliest
array[work_sheets] of int: last; % when to start latest
%array[work_sheets] of bool: mandratory; % is this work_sheet mandratory
array[work_sheets] of set of int: precedence; % which sheet needs to be done before which sheet, this should be in 
array[work_sheets] of int: duration;

set of int: work_sheets = 1..n_work_sheets; %index set used to later access the arrays
set of int: days = 1..horizon;
set of int: roads=1..l_roads;

% Decide when to start each worksheet
array[work_sheets] of var 1..horizon: t_w_k; % starting time of the worksheet, this we will branch on too

% constarint the starting time of the work sheet to be between the east and last
constraint forall(s in work_sheets)(t_w_k[s] <= last[s]);
constraint forall(s in work_sheets)(east[s] <= t_w_k[s]);

% precedence constraint between worksheets
constraint forall(s in work_sheets ,p in precedence[s])
                        (t_w_k[p] + duration[p] <= t_w_k[s]);

solve satisfy;

% Extra names to make minizinc shut up
%%%%%%%%%%%%%%%%%%
int : m_activities; % number of activities in the problem
array[activities] of int: activities_to_roads; % mapping form activities to roads
array[roads,days] of int: pertubation_cost ; % how much building on this day hurts; If this can be a funtion in minizinc make it so!
 array[work_sheets] of int: sheet_to_first_act; % mapping of worksheet to first activitiy
%array[work_sheets] of int: sheet_to_last_act; % mapping of worksheet to last activity
array[activities] of int: act_to_sheet; % mapping of activity to worksheet
set of int: set_sheet_to_first_act = {a|a in sheet_to_first_act};
set of int: activities = 1..m_activities;
%%%%%%%%%%%%%%%%%%