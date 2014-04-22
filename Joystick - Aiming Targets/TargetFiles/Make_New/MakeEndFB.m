%Make rotation files
clear all; close all; clc;
%Variables in Trial File
rotation = 0; %4
aiming_targets = 8;%2*4 = 8
target_ring = 0;%9
online_feedback = 0;%11
endpoint_feedback = 1;%12
binary_feedback = 1;%13
pause = 0;%14
show_score = 0;
goal = 2;%15 %1 - vector feedback, 2 - binary feedback, 3 - washout 
instruction = 1;%16 %1 - no instruction, 2 - nonspecific, 3 - specific
target_dist = 70;
numericfb = 1;

for subnum = 1:10
    %Number of trials
    numtrials = 8;
    
    %Target locations
    targets = [22.5:45:360]';
    distances= [target_dist*ones(1,length(targets))]';
    fb = [1,1,1,1,1,1,1,1]';
    td = [targets, distances, fb];
    numepics = numtrials/length(td);
    
    chk = 1;
    loopcount = 0;
    while chk > 0
        trialset = [];
        for i = 1:numepics
            temp = td(randperm(length(td)),:);
            trialset = [trialset;temp];
        end
        reps = find(diff(trialset(:,1)) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    totalset = length(trialset);
    header = {'trialnum','target_distance','target_angle','rotation',...
        'aiming_targets','target_ring','online_feedback','endpoint_feedback','binary_feedback',...
        'pause','show_score','goal','instruction','numericfb'};
    
    %Output columns
    %1. trialnum
    set(:,1) = [1:numtrials]';
    %2. target_distance
    set(:,2) = trialset(:,2);
    %3. target_angle
    set(:,3) = trialset(:,1);
    %4. rotation
    set(:,4) = repmat(rotation,numtrials,1);
    %5. aiming_targets
    set(:,5) = repmat(aiming_targets,numtrials,1);
    %6. target_ring
    set(:,6) = repmat(target_ring,numtrials,1);
    %7. online_feedback
    set(:,7) = repmat(online_feedback,numtrials,1);
    %8. endpoint_feedback
    set(:,8) = repmat(endpoint_feedback,numtrials,1);
    %9. binary_feedback
    set(:,9) = repmat(binary_feedback,numtrials,1);
    %10. pause
    set(:,10) = repmat(pause,numtrials,1);
    %11. show_score
    set(:,11) = repmat(show_score,numtrials,1);
    %12. goal
    set(:,12) = repmat(goal,numtrials,1);
    %13. instruction
    set(:,13) = repmat(instruction,numtrials,1);
    %14. numericfb
    set(:,14) = repmat(numericfb,numtrials,1);
    
    
    filename = strcat('BASEENDFB',num2str(subnum),'.tgt');
    %If you ever need strings in here use this way
    fid = fopen(filename,'wt');
    [rows,cols] = size(set);
    fprintf(fid,'%s\t',header{:});
    for i = 1:rows
        fprintf(fid,'\n');
        for j = 1:cols
            if j == 2
                fprintf(fid,'%3.1f\t',set(i,j));
            elseif j == 3
                fprintf(fid,'%3.1f\t',set(i,j));
            else
                fprintf(fid,'%3.1i\t',set(i,j));
            end
        end
    end
    fclose(fid)
end
