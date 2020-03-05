import dicom
import numpy
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt
import math

def CheckEligibility(RtPlan, FractionGroupNumber):
    EligibilityPlan=True#if a CP is not eligible, will turn to false
    BeamInPrescription=list()
    for prescription in RtPlan.FractionGroupSequence:
        if prescription.FractionGroupNumber == FractionGroupNumber:
            for BeamSequence in prescription.ReferencedBeamSequence:
                BeamInPrescription.append(BeamSequence.ReferencedBeamNumber)

    for BS in RtPlan.BeamSequence:
        if BS.BeamNumber in BeamInPrescription:
            EligibilityBeam=True
            for BLD in BS.BeamLimitingDeviceSequence:
                if BLD.RTBeamLimitingDeviceType == 'MLCX':
                   NbOfLeafPairs = BLD.NumberOfLeafJawPairs
                   LeafPosY = [float(i) for i in BLD.LeafPositionBoundaries]
                   #~ LeafPosY=LeafPosYtemp
                   #~ LeafPosY.extend(LeafPosYtemp)
                   
            JawPosX=[-1000,1000]
            JawPosY=[-1000,1000]
            for k,CP in enumerate(BS.ControlPointSequence):
                try:
                    BLDangle=float(CP.BeamLimitingDeviceAngle)
                except:
                    pass
                
                try:
                    for PositionSequence in CP.BeamLimitingDevicePositionSequence:
                        if PositionSequence.RTBeamLimitingDeviceType == 'ASYMX' or PositionSequence.RTBeamLimitingDeviceType == 'X':
                            JawPosX=[float(i) for i in PositionSequence.LeafJawPositions]
                        if PositionSequence.RTBeamLimitingDeviceType == 'ASYMY' or PositionSequence.RTBeamLimitingDeviceType == 'Y':
                            JawPosY=[float(i) for i in PositionSequence.LeafJawPositions]
                        if PositionSequence.RTBeamLimitingDeviceType == 'MLCX':
                            LeafPosX=[float(i) for i in PositionSequence.LeafJawPositions]
                except:
                    pass
                #verify that jaws are present
                if -1000 in JawPosX or -1000 in JawPosY:
                    print 'error, no jaws detected for beam ID',BS.BeamName, ' control point ',k
                    break
                LeafPosX1=LeafPosX[0:len(LeafPosX)/2]
                LeafPosX2=LeafPosX[len(LeafPosX)/2:]
                
                #creating a list of tuple containing every vertice coordinates
                MLCpoints = zip(LeafPosX1,LeafPosY[0:-1])
                MLCpoints.extend(zip(LeafPosX1,LeafPosY[1:]))
                MLCpoints.extend(zip(LeafPosX2,LeafPosY[0:-1]))
                MLCpoints.extend(zip(LeafPosX2,LeafPosY[1:]))
                
                #removing points behind jaws
                MLCpointsCleaned=list()
                for point in MLCpoints:
                    if point[0] >=JawPosX[0] and point[0] <= JawPosX[1] and point[1] >=JawPosY[0] and point[1] <= JawPosY[1]:
                        MLCpointsCleaned.append(point)
                MLCpoints=MLCpointsCleaned
                
                MLCpointsList=list(zip(*MLCpoints))
                
                #accepting maximum 24x24 field size
                FlatPanelPosition=[(-120.0,-120.0),(-120.0,120.0),(120.0,120.0),(120.0,-120.0)]
                FlatPanelPositionList=list(zip(*FlatPanelPosition))
                
                #rotating flat panel in the opposite direction instead of rotating every leaves in the right direction
                theta = -1.0*BLDangle * math.pi / 180.
                FlatPanelRotated = [ (x * math.cos(theta) - y * math.sin(theta), x * math.sin(theta) + y * math.cos(theta)) for x,y in FlatPanelPosition]
                FlatPanelPositionListRotated=list(zip(*FlatPanelRotated))

                #~ plt.scatter(MLCpointsList[0],MLCpointsList[1])
                #~ plt.scatter(FlatPanelPositionListRotated[0],FlatPanelPositionListRotated[1])
                #~ plt.show()

                path = mpltPath.Path(FlatPanelRotated)
                inside = path.contains_points(MLCpoints)
                if False in inside:
                    EligibilityBeam=False
                    EligibilityPlan=False
                    break
            #~ print 'Eligibility for beam ID ',BS.BeamName,' = ',EligibilityBeam
    #~ print 'Eligibility for plan= ',EligibilityPlan
    return EligibilityPlan
