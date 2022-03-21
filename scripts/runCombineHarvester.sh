# combineTool.py -M CollectLimits higgsCombineUnparSpin0_du1p5_LU2000.AsymptoticLimits.mH2000.root -o limitsUnparSpin0_du1p5_LU2000.json
# combineTool.py -M CollectLimits higgsCombineUnparSpin0_du1p5_LU2500.AsymptoticLimits.mH2500.root -o limitsUnparSpin0_du1p5_LU2500.json
# combineTool.py -M CollectLimits higgsCombineUnparSpin0_du1p5_LU3500.AsymptoticLimits.mH3500.root -o limitsUnparSpin0_du1p5_LU3500.json

# To combine by spin du
combineTool.py -M CollectLimits higgsCombineUnparSpin0_du1p5_LU*.AsymptoticLimits.m*.root -o limitsSpin0_du1p5.json
combineTool.py -M CollectLimits higgsCombineUnparSpin2_du1p5_LU*.AsymptoticLimits.m*.root -o limitsSpin2_du1p5.json
combineTool.py -M CollectLimits higgsCombineUnparSpin0_du1p1_LU*.AsymptoticLimits.m*.root -o limitsSpin0_du1p1.json
combineTool.py -M CollectLimits higgsCombineUnparSpin2_du1p1_LU*.AsymptoticLimits.m*.root -o limitsSpin2_du1p1.json
combineTool.py -M CollectLimits higgsCombineUnparSpin0_du1p9_LU*.AsymptoticLimits.m*.root -o limitsSpin0_du1p9.json
combineTool.py -M CollectLimits higgsCombineUnparSpin2_du1p9_LU*.AsymptoticLimits.m*.root -o limitsSpin2_du1p9.json
