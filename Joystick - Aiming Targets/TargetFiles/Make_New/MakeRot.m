%Make rotation files
clear all; close all; clc;

%Variables that don't change between blocks
rotation = 0; %4
aiming_targets = 8;%2*4 = 8
target_ring = 0;%9
pause = 0;%14
show_score = 0;
target_dist = 70;


for subnum = 1:10
    %FIRST 16 ARE BASELINE TRIALS===============================================
    %Variables that change between blocks
    rotation = 0; %4
    online_feedback = 0;%11
    endpoint_feedback = 0;%12
    binary_feedback = 1;%13
    goal = 2;%15 %1 - vector feedback, 2 - binary feedback, 3 - washout
    instruction = 1;%16 %1 - no instruction, 2 - nonspecific, 3 - specific
    numericfb=1;
    aiming_targets = 8;%2*4 = 8

    %Number of trials
    numtrials = 16;
    
    %Target locations
    targets = [22.5:45:360]';
    distances= [target_dist*ones(1,length(targets))]';
    td = [targets, distances];
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
    set1(:,1) = [1:numtrials]';
    %2. target_distance
    set1(:,2) = trialset(:,2);
    %3. target_angle
    set1(:,3) = trialset(:,1);
    %4. rotation
    set1(:,4) = repmat(rotation,numtrials,1);
    %5. aiming_targets
    set1(:,5) = repmat(aiming_targets,numtrials,1);
    %6. target_ring
    set1(:,6) = repmat(target_ring,numtrials,1);
    %7. online_feedback
    set1(:,7) = repmat(online_feedback,numtrials,1);
    %8. endpoint_feedback
    set1(:,8) = repmat(endpoint_feedback,numtrials,1);
    %9. binary_feedback
    set1(:,9) = repmat(binary_feedback,numtrials,1);
    %10. pause
    set1(:,10) = repmat(pause,numtrials,1);
    %11. show_score
    set1(:,11) = repmat(show_score,numtrials,1);
    %12. goal
    set1(:,12) = repmat(goal,numtrials,1);
    %13. instruction
    set1(:,13) = repmat(instruction,numtrials,1);
    %14. numericfb
    set1(:,14) = repmat(numericfb,numtrials,1);
    
    %NEXT ARE 120 ROTATION TRIALS==========================================
    %Variables that change between blocks
    rotation = -45; %4
    online_feedback = 0;%11
    endpoint_feedback = 0;%12
    binary_feedback = 1;%13
    goal = 2;%15 %1 - vector feedback, 2 - binary feedback, 3 - washout
    instruction = 1;%16 %1 - no instruction, 2 - nonspecific, 3 - specific
    aiming_targets = 8;%2*4 = 8
    numericfb = 1;

    %Number of trials
    numtrials = 120;
    
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
    set2(:,1) = [1:numtrials]';
    %2. target_distance
    set2(:,2) = trialset(:,2);
    %3. target_angle
    set2(:,3) = trialset(:,1);
    %4. rotation
    set2(:,4) = repmat(rotation,numtrials,1);
    %5. aiming_targets
    set2(:,5) = repmat(aiming_targets,numtrials,1);
    %6. target_ring
    set2(:,6) = repmat(target_ring,numtrials,1);
    %7. online_feedback
    set2(:,7) = repmat(online_feedback,numtrials,1);
    %8. endpoint_feedback
    set2(:,8) = repmat(endpoint_feedback,numtrials,1);
    %9. binary_feedback
    set2(:,9) = repmat(binary_feedback,numtrials,1);
    %10. pause
    set2(:,10) = repmat(pause,numtrials,1);
    %11. show_score
    set2(:,11) = repmat(show_score,numtrials,1);
    %12. goal
    set2(:,12) = repmat(goal,numtrials,1);
    %13. instruction
    set2(:,13) = repmat(instruction,numtrials,1);
    %14. numericfb
    set2(:,14) = repmat(numericfb,numtrials,1);
    
    
    %NEXT ARE WASHOUT TRIALS WITHOUT ANY FEEDBACK=======================
    %Variables that change between blocks
    rotation = 0; %4
    online_feedback = 0;%11
    endpoint_feedback = 0;%12
    binary_feedback = 0;%13
    goal = 3;%15 %1 - vector feedback, 2 - binary feedback, 3 - washout
    instruction = 1;%16 %1 - no instruction, 2 - nonspecific, 3 - specific
    numericfb=0;
    aiming_targets = 0;%2*4 = 8

    %Number of trials
    numtrials = 40;
    
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
    
    %Output columns
    %1. trialnum
    set3(:,1) = [1:numtrials]';
    %2. target_distance
    set3(:,2) = trialset(:,2);
    %3. target_angle
    set3(:,3) = trialset(:,1);
    %4. rotation
    set3(:,4) = repmat(rotation,numtrials,1);
    %5. aiming_targets
    set3(:,5) = repmat(aiming_targets,numtrials,1);
    %6. target_ring
    set3(:,6) = repmat(target_ring,numtrials,1);
    %7. online_feedback
    set3(:,7) = repmat(online_feedback,numtrials,1);
    %8. endpoint_feedback
    set3(:,8) = repmat(endpoint_feedback,numtrials,1);
    %9. binary_feedback
    set3(:,9) = repmat(binary_feedback,numtrials,1);
    %10. pause
    set3(:,10) = repmat(pause,numtrials,1);
    %11. show_score
    set3(:,11) = repmat(show_score,numtrials,1);
    %12. goal
    set3(:,12) = repmat(goal,numtrials,1);
    %13. instruction
    set3(:,13) = repmat(instruction,numtrials,1);
    %14. numericfb
    set3(:,14) = repmat(numericfb,numtrials,1);
    
    
    %NEXT ARE WASHOUT TRIALS WITH FEEDBACK==============================
    rotation = 0; %4
    online_feedback = 0;%11
    endpoint_feedback = 0;%12
    binary_feedback = 1;%13
    goal = 2;%15 %1 - vector feedback, 2 - binary feedback, 3 - washout
    instruction = 1;%16 %1 - no instruction, 2 - nonspecific, 3 - specific
    aiming_targets = 0;%2*4 = 8
    numericfb = 1;

    %Number of trials
    numtrials = 32;
    
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
    
    %Output columns
    %1. trialnum
    set4(:,1) = [1:numtrials]';
    %2. target_distance
    set4(:,2) = trialset(:,2);
    %3. target_angle
    set4(:,3) = trialset(:,1);
    %4. rotation
    set4(:,4) = repmat(rotation,numtrials,1);
    %5. aiming_targets
    set4(:,5) = repmat(aiming_targets,numtrials,1);
    %6. target_ring
    set4(:,6) = repmat(target_ring,numtrials,1);
    %7. online_feedback
    set4(:,7) = repmat(online_feedback,numtrials,1);
    %8. endpoint_feedback
    set4(:,8) = repmat(endpoint_feedback,numtrials,1);
    %9. binary_feedback
    set4(:,9) = repmat(binary_feedback,numtrials,1);
    %10. pause
    set4(:,10) = repmat(pause,numtrials,1);
    %11. show_score
    set4(:,11) = repmat(show_score,numtrials,1);
    %12. goal
    set4(:,12) = repmat(goal,numtrials,1);
    %13. instruction
    set4(:,13) = repmat(instruction,numtrials,1);
    %14. numericfb
    set4(:,14) = repmat(numericfb,numtrials,1);
    
    
    %DUMP IT INTO A FILE===================================================
    set = [set1;set2;set3;set4];
    set(:,1) = 1:size(set,1);
    
    header = {'trialnum','target_distance','target_angle','rotation',...
        'aiming_targets','target_ring','online_feedback','endpoint_feedback','binary_feedback',...
        'pause','show_score','goal','instruction','numericfb'};
    
    filename = strcat('ROT',num2str(subnum),'.tgt');
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
