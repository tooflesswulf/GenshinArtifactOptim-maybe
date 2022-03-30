# GenshinArtifactOptim-maybe
This project is kinda a mess. Current project is on a probabilistic modeling of artifact upgrade process, aiming to answer popular questions such as:
 - which artifact should I upgrade?
 - which character/artifact should I farm to replace?

## Python3 deps
`pip install numpy scipy`


## Demos
Example outputs for each demo item shown below. The warnings are the only things missing from a completely general/deployable solution, and all but the damage formula are already implemented in [fryzc's GenshinOptimizer](https://github.com/frzyc/genshin-optimizer).
- character/weapon stat load: We just need a way to convert the character & weapon to stats form (atk, def, base_atk, etc.) Already implemented in GO.
- set bonuses: handle this by baking it into the process of turning artifacts into stats. Already implemented in GO.
- damage formula/objective formula: I use the first and second derivatives of the objective in my implementation. Algebra for augmenting add/mult functions exists in [damage2.py](damage2.py).

### Artifact Upgrade Query
`python demo_artifact_upgrade.py`

```yaml
❯ python demo_artifact_upgrade.py

    ##########################################################
    ##                  DEMO 1.                             ##
    ##    Given a character and a single dmg objective,     ##
    ##   estimate the probability that upgrading a          ##
    ##   level 1 artifact will improve the objective.       ##
    ##########################################################
    
WARNING: characters stat load NOT IMPLEMENTED. Doing manual load.
 - diona LVL90
WARNING: weapon stat load NOT IMPLEMENTED. Doing manual load.
 - Prototype Crescent R5 LVL90 (passive on)
WARNING: damage formula loading NOT IMPLEMENTED. Manually entered
 - Diona Charge shot (no headshot) melt
WARNING: no set bonuses for this demo



Dionas current equipment:
LVL20 hp flower               LVL20 atk plume               LVL20 eleMas sands            LVL20 cryo_dmg_ goblet        LVL20 critRate_ circlet       
 - 33 atk                      - 16.2 enerRech_              - 538 hp                      - 4.7 hp_                     - 299 hp                     
 - 16 def                      - 37 def                      - 39 def                      - 11.1 atk_                   - 15.5 critDMG_              
 - 82 eleMas                   - 3.1 critRate_               - 12.4 critRate_              - 22.0 enerRech_              - 10.5 atk_                  
 - 14.0 critDMG_               - 19.4 critDMG_               - 7.8 critDMG_                - 16 eleMas                   - 56 eleMas                  

avg DMG (objective): 27887.184393283296


P ≈ 0.976
Expected dmg increase: 1081.9411980063805
LVL1 atk ViridescentVenerer plume
 - 299 hp
 - 5.8 atk_
 - 5.4 critDMG_
 - 21 eleMas

P ≈ 0.962
Expected dmg increase: 997.6335314420612
LVL1 atk BloodstainedChivalry plume
 - 4.7 atk_
 - 3.9 critRate_
 - 5.4 critDMG_

P ≈ 0.949
Expected dmg increase: 924.3496643639326
LVL1 atk OceanHuedClam plume
 - 3.1 critRate_
 - 6.2 critDMG_
 - 21 eleMas

P ≈ 0.492
Expected dmg increase: 319.1298770589192
LVL1 cryo_dmg_ BlizzardStrayer goblet
 - 19 def
 - 5.2 atk_
 - 18 atk
 ```


### Build Completeness Query
`python demo_build_rating.py`
```yaml
❯ python demo_build_rating.py

    ############################################################
    ##                  DEMO 2.                               ##
    ##    Given a character and a single dmg objective,       ##
    ##   estimate the probability that randomly farming       ##
    ##   a new flower/feather/etc will improve the objective  ##
    ############################################################
    
WARNING: characters stat load NOT IMPLEMENTED. Doing manual load.
 - diona LVL90
WARNING: weapon stat load NOT IMPLEMENTED. Doing manual load.
 - Prototype Crescent R5 LVL90 (passive on)
WARNING: damage formula loading NOT IMPLEMENTED. Manually entered
 - Diona Charge shot (no headshot) melt
WARNING: no set bonuses for this demo



Diona's current equipment:
LVL20 hp flower               LVL20 atk plume               LVL20 eleMas sands            LVL20 cryo_dmg_ goblet        LVL20 critRate_ circlet       
 - 33 atk                      - 16.2 enerRech_              - 538 hp                      - 4.7 hp_                     - 299 hp                     
 - 16 def                      - 37 def                      - 39 def                      - 11.1 atk_                   - 15.5 critDMG_              
 - 82 eleMas                   - 3.1 critRate_               - 12.4 critRate_              - 22.0 enerRech_              - 10.5 atk_                  
 - 14.0 critDMG_               - 19.4 critDMG_               - 7.8 critDMG_                - 16 eleMas                   - 56 eleMas                  

avg DMG: 27887.184393283296


Probability that a new XXX will improve the objective
flower  0.01868
plume   0.19687
sands   0.00439
goblet  0.02729
circlet 0.00024


Expected num artifacts farmed to improve objective: 20.204345501603534
```





