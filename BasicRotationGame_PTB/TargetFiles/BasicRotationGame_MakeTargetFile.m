%Make rotation files
clear all; close all; clc;

%Variables that don't change between blocks
target_dist = 70;
NumOnlineBase = 16;
NumEPBase = 32;
NumBaseNoFB = 16;
rotation = 45;
NumPreRot = 24;
NumRotationTrials = 240;
%Target locations
targets = [0;45;90;135;180;225;270;315'];
NumWashoutTrials=16;
StartSubNum = 1;
NumSubs = 10;
aim_ring = 1;
TotalTrials = NumOnlineBase+NumEPBase+NumBaseNoFB+NumPreRot+NumRotationTrials+NumWashoutTrials;


for subnum = 1:NumSubs
    %FIRST ARE Online BASELINE TRIALS===============================================
    %Variables that change between blocks
    online_feedback = 1;
    endpoint_feedback = 1;
    trialset = [];
    %online base
    chk = 1;
    loopcount = 0;
    numepics = NumOnlineBase/((size(targets,1))*(size(targets,2)));%we are only using 16 out of 24 for each run
    while chk > 0
        temptrialset = trialset;
        for i = 1:numepics
            temp = targets(randperm(length(targets)))';
            temptrialset = [temptrialset temp];
        end
        reps = find(diff(temptrialset) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    trialset=temptrialset;

    %endpont base
    chk = 1;
    loopcount = 0;
    numepics = NumEPBase/((size(targets,1))*(size(targets,2)));%we are only using 16 out of 24 for each run
    while chk > 0
        temptrialset = trialset;
        for i = 1:numepics
            temp = targets(randperm(length(targets)))';
            temptrialset = [temptrialset temp];
        end
        reps = find(diff(temptrialset) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    trialset=temptrialset;
    
    %washoutbase no FB. Using off axis targets first
    chk = 1;
    loopcount = 0;
     numepics = NumBaseNoFB/((size(targets,1))*(size(targets,2)));%we are only using 16 out of 24 for each run
    while chk > 0
        temptrialset = trialset;
        for i = 1:numepics
            temp = targets(randperm(length(targets)))';
            temptrialset = [temptrialset temp];
        end
        reps = find(diff(temptrialset) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    trialset=temptrialset;
    
    %num prerot base
    chk = 1;
    loopcount = 0;
    numepics = NumPreRot/((size(targets,1))*(size(targets,2)));
    while chk > 0
        temptrialset = trialset;
        for i = 1:numepics
            temp = targets(randperm(length(targets)))';
            temptrialset = [temptrialset temp];
        end
        reps = find(diff(temptrialset) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    trialset=temptrialset;
    
    %num NumRotationTrials
    chk = 1;
    loopcount = 0;
    numepics = NumRotationTrials/((size(targets,1))*(size(targets,2)));
    while chk > 0
        temptrialset = trialset;
        for i = 1:numepics
            temp = targets(randperm(length(targets)))';
            temptrialset = [temptrialset temp];
        end
        reps = find(diff(temptrialset) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    trialset=temptrialset;
    
    %washout 
     chk = 1;
    loopcount = 0;
     numepics = NumWashoutTrials/((size(targets,1))*(size(targets,2)));%we are only using 16 out of 24 for each run
    while chk > 0
        temptrialset = trialset;
        for i = 1:numepics
            temp = targets(randperm(length(targets)))';
            temptrialset = [temptrialset temp];
        end
        reps = find(diff(temptrialset) == 0);
        if isempty(reps);
            chk = 0;
            loopcount
        end
        loopcount = loopcount + 1;
    end
    trialset=temptrialset;
    
    if NumOnlineBase > 0
        trial_rotation(1:NumOnlineBase) = 0;
    end
    if NumEPBase > 0
        trial_rotation(NumOnlineBase+1:NumOnlineBase+NumEPBase) = 0;
    end
    if NumBaseNoFB > 0
        trial_rotation(NumOnlineBase+NumEPBase+1:NumOnlineBase+NumEPBase+NumBaseNoFB) = 0;
    end
    if NumPreRot > 0
        trial_rotation(NumOnlineBase+NumEPBase+NumBaseNoFB+1:NumPreRot+NumOnlineBase+NumEPBase+NumBaseNoFB) = 0;
    end
    
    trial_rotation((NumEPBase+NumOnlineBase+NumPreRot+NumBaseNoFB+1):(NumRotationTrials+NumEPBase+NumOnlineBase+NumPreRot+NumBaseNoFB))=rotation;
    
    trial_rotation((TotalTrials-NumWashoutTrials+1):TotalTrials)=0;
    
    
    totalset = length(trialset);
    header = {'trials','endpoint_feedback','online_feedback','aim_report',...
        'aim_ring','rotation','instruction','target_angle','target_dist'};
    
    %Output columns
    %1. trialnum
    set1(:,1) = [1:TotalTrials]';
    %2. endpoint_feedback
    set1(:,2) = repmat(1,TotalTrials,1);
    set1(NumOnlineBase+NumEPBase+1:NumOnlineBase+NumEPBase+NumBaseNoFB,2) = repmat(0,(NumBaseNoFB),1);    
    set1(TotalTrials-NumWashoutTrials+1:TotalTrials,2) = repmat(0,(NumWashoutTrials),1);    
    %3. online_feedback
    set1(:,3) = repmat(0,TotalTrials,1);
    set1(1:NumOnlineBase,3) = repmat(1,(NumOnlineBase),1);
    %4. aim_report
    set1(:,4) = repmat(1,TotalTrials,1);
    set1(1:NumOnlineBase+NumEPBase+NumBaseNoFB,4) = repmat(0,(NumOnlineBase+NumEPBase+NumBaseNoFB),1);
    set1(TotalTrials-NumWashoutTrials+1:TotalTrials,4) = repmat(0,(NumWashoutTrials),1);
    %5 aim_ring
    set1(:,5) = repmat(aim_ring,TotalTrials,1);
    %6 Rotation
    if subnum<=NumSubs/2 %flip rotation for second half
        set1(:,6) = [trial_rotation'];
    else
        set1(:,6) = [-trial_rotation'];
    end
    %7 instruction
    set1(:,7) = repmat(0,TotalTrials,1);
    set1(NumOnlineBase,7) = 1;
    set1(NumOnlineBase+NumEPBase,7) = 3;
    set1(NumOnlineBase+NumEPBase+NumBaseNoFB,7) = 2;
    set1(TotalTrials-NumWashoutTrials,7) = 3;
    %8 target_angle
    set1(:,8) = trialset(1:TotalTrials);
    %9 target dist
    set1(:,9) = repmat(target_dist,TotalTrials,1);
    
    
    
    %DUMP IT INTO A FILE===================================================
    set = [set1];
    set(:,1) = 1:size(set,1);
    
    
    filename = strcat('BasicRotationGame',num2str(subnum+StartSubNum-1),'.tgt');
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
            elseif j == 4
                fprintf(fid,'%3.4f\t',set(i,j));
                
            else
                fprintf(fid,'%3.1i\t',set(i,j));
            end
        end
    end
    fclose(fid)
end
