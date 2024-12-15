using System.Collections.Generic;
using System.Linq;
using GameManager.EnumTypes;
using GameManager.GameElements;
using UnityEngine;

/////////////////////////////////////////////////////////////////////////////
// This is the Moron Agent
/////////////////////////////////////////////////////////////////////////////

namespace GameManager
{
    ///<summary>Planning Agent is the over-head planner that decided where
    /// individual units go and what tasks they perform.  Low-level 
    /// AI is handled by other classes (like pathfinding).
    ///</summary> 
    public class PlanningAgent : Agent
    {
        //Semi constants
        private int maxWorkerCount = 20;
        private int maxSoldierCount = 15;
        private int maxRefineries = 3;
        private int maxBarracks = 4;
        private float targetGold = 500;


        //For changing semi constants
		int changeValue = 1;
		int goldChangeValue = 50;
        int roundNum = 0;
        int wins = 0;
        int lastLoopRandom = 0;
        int totalLoops = 0;
        int totalRandomCount = 0;
        int currentValueIteration = 0;

        //For storing first maximum
        Dictionary<string, float> FirstMaximum;
        Dictionary<string, float> StartVals;

		bool compareToResetDict = false;

        //Which direction we're going 
        //For this value -1 means decreasing, 1 means increasing, 0 means it's unassigned aka first run 
        private int increasing = 0;

        //For when we change directions on a given metric
        private int timesFlipped = 0;

        //For tracking our successes and failures
        //Int key for first dictionary keeps track of iteration 
        //Value for first dictionary contains another dictionary which will contain all metrics and value to attain those
        Dictionary<int, Dictionary<string, float>> QList = new Dictionary<int, Dictionary<string, float>>();


		enum LearnValue { Workers, Soldiers, Refineries, Barracks, TargetGold};
		//For learning purposes
		/*
        private int myTotalTrainedWorkers = 0;
        private int myTotalTrainedSoldiers = 0;
        private int myTotalTrainedArchers = 0;
        private int enemyTotalTrainedWorkers = 0;
        private int enemyTotalTrainedSoldiers = 0;
        private int enemyTotalTrainedArchers = 0;
        */
		enum AgentState {InitialBuild, ArmyBuilding, Attacking, GatherResources};
        private AgentState state = AgentState.InitialBuild;
        private LearnValue learnValue = LearnValue.Workers;

        #region Private Data

        ///////////////////////////////////////////////////////////////////////
        // Handy short-cuts for pulling all of the relevant data that you
        // might use for each decision.  Feel free to add your own.
        ///////////////////////////////////////////////////////////////////////

        /// <summary>
        /// The enemy's agent number
        /// </summary>
        private int enemyAgentNbr { get; set; }

        /// <summary>
        /// My primary mine number
        /// </summary>
        private int mainMineNbr { get; set; }

        /// <summary>
        /// My primary base number
        /// </summary>
        private int mainBaseNbr { get; set; }

        /// <summary>
        /// List of all the mines on the map
        /// </summary>
        private List<int> mines { get; set; }

        /// <summary>
        /// List of all of my workers
        /// </summary>
        private List<int> myWorkers { get; set; }

        /// <summary>
        /// List of all of my soldiers
        /// </summary>
        private List<int> mySoldiers { get; set; }

        /// <summary>
        /// List of all of my archers
        /// </summary>
        private List<int> myArchers { get; set; }

        /// <summary>
        /// List of all of my bases
        /// </summary>
        private List<int> myBases { get; set; }

        /// <summary>
        /// List of all of my barracks
        /// </summary>
        private List<int> myBarracks { get; set; }

        /// <summary>
        /// List of all of my refineries
        /// </summary>
        private List<int> myRefineries { get; set; }

        /// <summary>
        /// List of the enemy's workers
        /// </summary>
        private List<int> enemyWorkers { get; set; }

        /// <summary>
        /// List of the enemy's soldiers
        /// </summary>
        private List<int> enemySoldiers { get; set; }

        /// <summary>
        /// List of enemy's archers
        /// </summary>
        private List<int> enemyArchers { get; set; }

        /// <summary>
        /// List of the enemy's bases
        /// </summary>
        private List<int> enemyBases { get; set; }

        /// <summary>
        /// List of the enemy's barracks
        /// </summary>
        private List<int> enemyBarracks { get; set; }

        /// <summary>
        /// List of the enemy's refineries
        /// </summary>
        private List<int> enemyRefineries { get; set; }

        /// <summary>
        /// List of the possible build positions for a 3x3 unit
        /// </summary>
        private List<Vector3Int> buildPositions { get; set; }

        /// <summary>
        /// Finds all of the possible build locations for a specific UnitType.
        /// Currently, all structures are 3x3, so these positions can be reused
        /// for all structures (Base, Barracks, Refinery)
        /// Run this once at the beginning of the game and have a list of
        /// locations that you can use to reduce later computation.  When you
        /// need a location for a build-site, simply pull one off of this list,
        /// determine if it is still buildable, determine if you want to use it
        /// (perhaps it is too far away or too close or not close enough to a mine),
        /// and then simply remove it from the list and build on it!
        /// This method is called from the Awake() method to run only once at the
        /// beginning of the game.
        /// </summary>
        /// <param name="unitType">the type of unit you want to build</param>
        public void FindProspectiveBuildPositions(UnitType unitType)
        {
            // For the entire map
            for (int i = 0; i < GameManager.Instance.MapSize.x; ++i)
            {
                for (int j = 0; j < GameManager.Instance.MapSize.y; ++j)
                {
                    // Construct a new point near gridPosition
                    Vector3Int testGridPosition = new Vector3Int(i, j, 0);

                    // Test if that position can be used to build the unit
                    if (Utility.IsValidGridLocation(testGridPosition)
                        && GameManager.Instance.IsBoundedAreaBuildable(unitType, testGridPosition))
                    {
                        // If this position is buildable, add it to the list
                        buildPositions.Add(testGridPosition);
                    }
                }
            }
        }

        /// <summary>
        /// Build a building
        /// </summary>
        /// <param name="unitType"></param>
        /// <param name="Base" ></param>
        public void BuildBuilding(UnitType unitType, bool Base = false)
        {
            if (!Base)
            {
                // For each worker
                foreach (int worker in myWorkers)
                {
                    // Grab the unit we need for this function
                    Unit unit = GameManager.Instance.GetUnit(worker);

                    // Make sure this unit actually exists and we have enough gold
                    if (unit != null && Gold >= Constants.COST[unitType])
                    {
                        // Find the closest build position to this worker's position (DUMB) and 
                        float dist = float.MaxValue;
                        Vector3Int pos = buildPositions[0];
                        // build the base there
                        foreach (Vector3Int toBuild in buildPositions)
                        {
                            if (GameManager.Instance.IsBoundedAreaBuildable(unitType, toBuild))
                            {
                                if ((new Vector3(toBuild.x, toBuild.y, toBuild.z) - unit.GridPosition).magnitude < dist)
                                {
                                    dist = (new Vector3(toBuild.x, toBuild.y, toBuild.z) - unit.GridPosition).magnitude;
                                    pos = toBuild;
                                }
                            }
                        }
                        if (pos != null)
                        {
                            Build(unit, pos, unitType);
                        }
                    }
                }
            }
            else
            {
                //Get the initial worker
                if(myWorkers.Count == 0)
                    return;
                Unit initilWorker = GameManager.Instance.GetUnit(myWorkers[0]);
                

                //Find the mine that's closest to this worker
                int closeMine = -1;
                closeMine = FindClosestUnit(myWorkers[0], mines);
                if(closeMine != -1)
                {
                    Unit CloseMineUnit = GameManager.Instance.GetUnit(closeMine);
                    float dist = float.MaxValue;
                    Vector3Int pos = buildPositions[0];
                    foreach(Vector3Int toBuild in buildPositions)
                    {
                        if(GameManager.Instance.IsBoundedAreaBuildable(unitType, toBuild))
                        {
                            if((new Vector3(toBuild.x,toBuild.y, toBuild.z) - CloseMineUnit.GridPosition).magnitude < dist)
                            {
								dist = (new Vector3(toBuild.x, toBuild.y, toBuild.z) - CloseMineUnit.GridPosition).magnitude;
								pos = toBuild;
							}
                        }
                    }
                    if (pos != null)
                    {
                        Build(initilWorker, pos, unitType);
                    }
                }
            }
        }

        /// <summary>
        /// Attack the enemy
        /// </summary>
        /// <param name="myTroops"></param>
        public void AttackEnemy(List<int> myTroops)
        {
            if (myTroops.Count > 3)
            {
                // For each of my troops in this collection
                foreach (int troopNbr in myTroops)
                {
                    // If this troop is idle, give him something to attack
                    Unit troopUnit = GameManager.Instance.GetUnit(troopNbr);
                    if (troopUnit.CurrentAction == UnitAction.IDLE)
                    {
                        // If there are archers to attack
                        if (enemyArchers.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyArchers[UnityEngine.Random.Range(0, enemyArchers.Count)]));
                        }
                        // If there are soldiers to attack
                        else if (enemySoldiers.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemySoldiers[UnityEngine.Random.Range(0, enemySoldiers.Count)]));
                        }
                        // If there are workers to attack
                        else if (enemyWorkers.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyWorkers[UnityEngine.Random.Range(0, enemyWorkers.Count)]));
                        }
                        // If there are bases to attack
                        else if (enemyBases.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyBases[UnityEngine.Random.Range(0, enemyBases.Count)]));
                        }
                        // If there are barracks to attack
                        else if (enemyBarracks.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyBarracks[UnityEngine.Random.Range(0, enemyBarracks.Count)]));
                        }
                        // If there are refineries to attack
                        else if (enemyRefineries.Count > 0)
                        {
                            Attack(troopUnit, GameManager.Instance.GetUnit(enemyRefineries[UnityEngine.Random.Range(0, enemyRefineries.Count)]));
                        }
                    }
                }
            }
            else if (myTroops.Count > 0)
            {
                // Find a good rally point
                Vector3Int rallyPoint = Vector3Int.zero;
                foreach (Vector3Int toBuild in buildPositions)
                {
                    if (GameManager.Instance.IsBoundedAreaBuildable(UnitType.BASE, toBuild))
                    {
                        rallyPoint = toBuild;
                        // For each of my troops in this collection
                        foreach (int troopNbr in myTroops)
                        {
                            // If this troop is idle, give him something to attack
                            Unit troopUnit = GameManager.Instance.GetUnit(troopNbr);
                            if (troopUnit.CurrentAction == UnitAction.IDLE)
                            {
                                Move(troopUnit, rallyPoint);
                            }
                        }
                        break;
                    }
                }
            }
        }
        #endregion

        #region Public Methods

        private void ChangeValueRandom(LearnValue changeValue)
        {
			switch (changeValue)
			{
				case LearnValue.Workers:
					maxWorkerCount = Random.Range(0, 40);
					break;
				case LearnValue.Soldiers:
					maxSoldierCount = Random.Range(0, 40);
					break;
				case LearnValue.Refineries:
					maxRefineries = Random.Range(0, 40);
					break;
				case LearnValue.Barracks:
					maxBarracks = Random.Range(0, 40);
					break;
				case LearnValue.TargetGold:
					targetGold = Random.Range(100, 2000);
					break;
			}
		}

        private int CalculateWin()
        {
			if (AgentNbrWins > wins)
			{
				wins++;
                return 1;
			}
			else
			{
                return -1;
			}
		}

        private void SwitchLearnValue()
        {
			//Switch which value is being learned
			switch (learnValue)
			{
				case LearnValue.Workers:
					learnValue = LearnValue.Soldiers;
					break;
				case LearnValue.Soldiers:
					learnValue = LearnValue.Refineries;
					break;
				case LearnValue.Refineries:
					learnValue = LearnValue.Barracks;
					break;
				case LearnValue.Barracks:
					learnValue = LearnValue.TargetGold;
					break;
				case LearnValue.TargetGold:
					learnValue = LearnValue.Workers;
					break;
			}
		}

        private void SetValuesToDictValues(Dictionary<string, float> values)
        {
            //Setting the values to input dictionary values
			maxWorkerCount = (int)values["MaxWorkersValue"];
			maxSoldierCount = (int)values["MaxSoldierValue"];
			maxRefineries = (int)values["MaxRefineriesValue"];
			maxBarracks = (int)values["MaxBarracksValue"];
			targetGold = (int)values["TargetGoldValue"];
		}

        private void IncrementValues(int increasing)
        {
			switch (learnValue)
			{

				case LearnValue.Workers:
					maxWorkerCount = maxWorkerCount + (increasing * changeValue);
					break;
				case LearnValue.Soldiers:
					maxSoldierCount = maxSoldierCount + (increasing * changeValue);
					break;
				case LearnValue.Refineries:
					maxRefineries = maxRefineries + (increasing * changeValue);
					break;
				case LearnValue.Barracks:
					maxBarracks = maxBarracks + (increasing * changeValue);
					break;
				case LearnValue.TargetGold:
					targetGold = targetGold + (increasing * goldChangeValue);
					break;
			}
		}

        private void WriteToDebugFile(int wonGame, float fitness, float increaseByRandom)
        {
			Log("Max Workers Value: " + maxWorkerCount);
			Log("Max Soldier Value: " + maxSoldierCount);
			Log("Max Refineries Value: " + maxRefineries);
			Log("Max Barracks Valeu: " + maxBarracks);
			Log("Target Gold Value: " + targetGold);
			Log("Did we win: " + wonGame);
			Log("Time to end: " + GameManager.Instance.TotalGameTime);
			Log("Fitness: " + fitness);
			Log("Value Changing: " + learnValue.ToString());
			Log("Increasing By Random: " + increaseByRandom);
		}



        /// <summary>
        /// Called at the end of each round before remaining units are
        /// destroyed to allow the agent to observe the "win/loss" state
        /// </summary>
        public override void Learn()
        {
            Debug.Log("Nbr Wins: " + AgentNbrWins);

            //Calculate if won the game
			int wonGame =  CalculateWin();			

			//Calculate fitness
			//Less time to finish game gets more points
			//Winning gives a lot of points losing takes away a lot of points
			float fitness = (GameManager.Instance.MaxNbrOfSeconds - GameManager.Instance.TotalGameTime) + (wonGame * 1000f);

			//Saving all the information in the dictionary
			Dictionary<string, float> values = new Dictionary<string, float>
			{
				{ "MaxWorkersValue", maxWorkerCount},
				{ "MaxSoldierValue", maxSoldierCount},
				{ "MaxRefineriesValue", maxRefineries},
				{ "MaxBarracksValue", maxBarracks},
				{ "TargetGoldValue" , targetGold },
				{ "GameTime", GameManager.Instance.TotalGameTime },
				{ "Win" , wonGame },
				{ "Fitness" , fitness },
				{ "IncreaseByRandom:" , 0 }
			};

			//Every 5 loops random a value
			if (totalLoops - lastLoopRandom >= 5)
			{
                //Sets the last loop random to this loop iteration
                lastLoopRandom = totalLoops;
                //Sets the value for proper output 
				values["IncreaseByRandom:"] = 1;
                //Randoms a value
                ChangeValueRandom((LearnValue)(totalRandomCount % 5));
			}

            //Debug.Log("PlanningAgent::Learn");
            WriteToDebugFile(wonGame, fitness, values["IncreaseByRandom:"]);

            //Since we haven't added our new results to this dictionary if it's the first 
            //test of a given learnValue we need to save a reference to where it will be added
            //At the end of this method
            if (currentValueIteration == 0)
            {
                //Do special shit for round 1 
                if (roundNum == 1)
                {
                    StartVals = values;
                    increasing = 0;
                }
                else
                {
                    StartVals = QList[QList.Count - 1];
                    increasing = 0;
                }
            }
            currentValueIteration++;
         

            //If on first iteration we need special handling to avoid index out of bounds
            if(increasing == 0)
            {
                //Increase or decrease randomly
                if(Random.Range(0,1) >= 0.5)
                {
                    increasing = 1;
                }
                else
                {
                    increasing = -1;
                }
                //Increment the values
				IncrementValues(increasing);
			}
            //Otherwise compare like normal
            else
            {
                //Getting the correct dictionary to compare to
                Dictionary<string, float> compareDict = new Dictionary<string, float>();
                if(!compareToResetDict)
                {
                    compareDict = QList[roundNum - 1];
                }
                else
                {
                    compareDict = StartVals;
				}

                //If fitness is worse than the compared dictionary take the appropriate action
                if(fitness < compareDict["Fitness"])
                {
					//Incrementing times we've flipped and setting increasing to opposite
					timesFlipped++;
					increasing *= -1;
					//On First flip save reference to local maximum to check against other side results
					if (timesFlipped == 1)
					{
						//Saving a reference to this maximum
						FirstMaximum = QList[roundNum - 1];
						//Set compare to reset dict to compare to correct dictionary
						compareToResetDict = true;
                        //Resetting the values 
                        SetValuesToDictValues(StartVals);
					}
					else
					{
						//Compare results from first max to this new found max
						if (values["Fitness"] > FirstMaximum["Fitness"])
						{
                            //When new max is greater set that to be new values
                            SetValuesToDictValues(QList[roundNum-1]);
						}
						else
						{
                            //When first max is greater set that to be new values
                            SetValuesToDictValues(FirstMaximum);
						}

						//Resetting currentValue Iteration 
						currentValueIteration = 0;

                        //Switching learn value
                        SwitchLearnValue();
					}
				}
				IncrementValues(increasing);
			}
			//Saving the dictionary of values for later use
			QList.Add(roundNum, values);
		}

        /// <summary>
        /// Called before each match between two agents.  Matches have
        /// multiple rounds. 
        /// </summary>
        public override void InitializeMatch()
        {
            Debug.Log("Moron's: " + AgentName);
            //Debug.Log("PlanningAgent::InitializeMatch");
        }

        /// <summary>
        /// Called at the beginning of each round in a match.
        /// There are multiple rounds in a single match between two agents.
        /// </summary>
        public override void InitializeRound()
        {
			//Debug.Log("PlanningAgent::InitializeRound");
			buildPositions = new List<Vector3Int>();

            roundNum++;

            FindProspectiveBuildPositions(UnitType.BASE);

            // Set the main mine and base to "non-existent"
            mainMineNbr = -1;
            mainBaseNbr = -1;

            // Initialize all of the unit lists
            mines = new List<int>();

            myWorkers = new List<int>();
            mySoldiers = new List<int>();
            myArchers = new List<int>();
            myBases = new List<int>();
            myBarracks = new List<int>();
            myRefineries = new List<int>();

            enemyWorkers = new List<int>();
            enemySoldiers = new List<int>();
            enemyArchers = new List<int>();
            enemyBases = new List<int>();
            enemyBarracks = new List<int>();
            enemyRefineries = new List<int>();
        }

        /// <summary>
        /// Calculates the closest unit from a start 
        /// </summary>
        /// <param name="startUnit"></param>
        /// <param name="units"></param>
        /// <returns></returns>
        private int FindClosestUnit(int startUnit, List<int> units)
        {
            float dist = float.MaxValue;
            Unit sUnit = GameManager.Instance.GetUnit(startUnit);
            int result = -1;
            foreach(int unit in units)
            {
                Unit unitObj = GameManager.Instance.GetUnit(unit);
                Vector3 distVec = sUnit.GridPosition - unitObj.GridPosition;
                if(distVec.magnitude < dist)
                {
                    result = unit;
                    dist = distVec.magnitude;
                }
            }
            return result;
        }

        /// <summary>
        /// Updates the game state for the Agent - called once per frame for GameManager
        /// Pulls all of the agents from the game and identifies who they belong to
        /// </summary>
        public void UpdateGameState()
        {
            // Update the common resources
            mines = GameManager.Instance.GetUnitNbrsOfType(UnitType.MINE);

            // Update all of my unitNbrs
            myWorkers = GameManager.Instance.GetUnitNbrsOfType(UnitType.WORKER, AgentNbr);
            mySoldiers = GameManager.Instance.GetUnitNbrsOfType(UnitType.SOLDIER, AgentNbr);
            myArchers = GameManager.Instance.GetUnitNbrsOfType(UnitType.ARCHER, AgentNbr);
            myBarracks = GameManager.Instance.GetUnitNbrsOfType(UnitType.BARRACKS, AgentNbr);
            myBases = GameManager.Instance.GetUnitNbrsOfType(UnitType.BASE, AgentNbr);
            myRefineries = GameManager.Instance.GetUnitNbrsOfType(UnitType.REFINERY, AgentNbr);

            // Update the enemy agents & unitNbrs
            List<int> enemyAgentNbrs = GameManager.Instance.GetEnemyAgentNbrs(AgentNbr);
            if (enemyAgentNbrs.Any())
            {
                enemyAgentNbr = enemyAgentNbrs[0];
                enemyWorkers = GameManager.Instance.GetUnitNbrsOfType(UnitType.WORKER, enemyAgentNbr);
                enemySoldiers = GameManager.Instance.GetUnitNbrsOfType(UnitType.SOLDIER, enemyAgentNbr);
                enemyArchers = GameManager.Instance.GetUnitNbrsOfType(UnitType.ARCHER, enemyAgentNbr);
                enemyBarracks = GameManager.Instance.GetUnitNbrsOfType(UnitType.BARRACKS, enemyAgentNbr);
                enemyBases = GameManager.Instance.GetUnitNbrsOfType(UnitType.BASE, enemyAgentNbr);
                enemyRefineries = GameManager.Instance.GetUnitNbrsOfType(UnitType.REFINERY, enemyAgentNbr);
                Debug.Log("<color=red>Enemy gold</color>: " + GameManager.Instance.GetAgent(enemyAgentNbr).Gold);
            }
        }

        /// <summary>
        /// Update the GameManager - called once per frame
        /// </summary>
        public override void Update()
        {
            UpdateGameState();

            Dictionary<string, float> dict = UpdateHeuristics();

            float maxValue = float.MinValue;
            string bestAction = "";
            foreach(KeyValuePair<string, float> kvp in dict)
            {
                if (kvp.Value > maxValue)
                {
                    maxValue = kvp.Value;
                    bestAction = kvp.Key;                    
                }
            }

            Debug.LogWarning("Best Action is: " + bestAction);
            string ovride = "";
            switch(bestAction)
            {
                case "BaseBuild":
                    state = AgentState.InitialBuild;
                    ovride = bestAction;
                    break;
                case "Worker":
                    state = AgentState.InitialBuild;
                    ovride = bestAction;
                    break;
                case "BarrackBuild":
                    state = AgentState.InitialBuild;
					ovride = bestAction;
					break;
                case "ArmyBuild":
                    state = AgentState.ArmyBuilding;
                    break;
                case "Attack":
                    state = AgentState.Attacking;
                    break;
                case "GatherGoldHeur":
                    state = AgentState.InitialBuild;
                    ovride = "GatherGold";
					break;
                case "Refine":
                    state = AgentState.InitialBuild;
                    ovride = bestAction;
                    break;
                case "":
                    //Debug.LogWarning("Not best action go Fuck thyself");
                    break;
			}
            
			switch (state)
            {
                case AgentState.InitialBuild:
                    BuildBase(ovride);                    
                    if (myBases.Count > 0 && myBarracks.Count > 2 && myRefineries.Count > 2)
                    {
                        state = AgentState.ArmyBuilding;
                    }
                break;
                case AgentState.ArmyBuilding:
                    BuildArmy();
                    GatherGold();
                    if (myBases.Count == 0 || myBarracks.Count == 0 || myRefineries.Count == 0)
                    {
                        state = AgentState.InitialBuild;
                    }
                    
                break;
                case AgentState.Attacking:
                    GatherGold();
                    Attack();                    
                    if (myArchers.Count + mySoldiers.Count < enemyArchers.Count + enemySoldiers.Count)
                    {
                        state = AgentState.ArmyBuilding;
                    }                    
                break;
            }
        }

        private Dictionary<string, float> UpdateHeuristics()
        {
            Dictionary<string, float> heuristicsDict = new Dictionary<string, float>
            {
                { "BaseBuild", CalcBaseHeur() },
                { "Worker", CalcWorkerHeur() },
                { "BarrackBuild", CalcBarrackHeur() },
				{ "Refine" , CalcRefHeur() },
				{ "ArmyBuild", CalcArmyHeur()},
                { "Attack", CalcAttackHeur()},
                { "GatherGold" , GatherGoldHeur()},                
			};

			// Print dictionary efficiently
			foreach (var entry in heuristicsDict)
			{
				Debug.LogWarning(($"{entry.Key} {entry.Value}"));
			}

			return heuristicsDict;
        }

        private float CalcWorkerHeur()
        {
            float workerHeur = Mathf.Clamp(maxWorkerCount - myWorkers.Count, 0, 1);
            float goldCheck = Mathf.Clamp(Gold - Constants.COST[UnitType.WORKER], 0, 1);

            return workerHeur * goldCheck;
        }

        private float CalcBaseHeur()
        {
			float baseHeur = Mathf.Clamp(1 - myBases.Count, 0, 1);
			float goldCheck = Mathf.Clamp(Gold - Constants.COST[UnitType.BASE], 0, 1);

			return baseHeur * goldCheck;
		}

        private float CalcBarrackHeur()
        {
            float barrHeur = Mathf.Clamp(1 - myBarracks.Count, 0, 1);
            float goldCheck = Mathf.Clamp(Gold - Constants.COST[UnitType.BARRACKS], 0, 1);
            float barrVsOpp = Mathf.Clamp(enemyBarracks.Count - myBarracks.Count, 0, 1);

            return Mathf.Clamp((barrHeur + barrVsOpp) * goldCheck, 0, 1);
        }

        private float CalcArmyHeur()
        {
            float targetArmySize = 15f;
            float armyHeur = Mathf.Clamp(targetArmySize - mySoldiers.Count + myArchers.Count, 0, 1);
            float armyVsOpp = Mathf.Clamp((enemyArchers.Count + enemySoldiers.Count) - (mySoldiers.Count + myArchers.Count), 0, 1);
            float goldCheck = Mathf.Clamp(Gold - Constants.COST[UnitType.SOLDIER], 0, 1);

            return Mathf.Clamp((armyHeur + armyVsOpp) * goldCheck, 0, 1);
		}

        private float CalcAttackHeur()
        {
            return Mathf.Clamp((myArchers.Count + mySoldiers.Count) - (enemySoldiers.Count + enemyArchers.Count), 0, 1);
        }

        private float GatherGoldHeur()
        {
            return Mathf.Clamp(targetGold - Gold, 0, 1);
        }

        private float CalcRefHeur()
        {
            float refHeur = Mathf.Clamp(1 - myRefineries.Count, 0, 1);
            float goldCheck = Mathf.Clamp(Gold - Constants.COST[UnitType.REFINERY], 0, 1);

            return refHeur * goldCheck;
		}

        private void BuildBase(string ovride = "")
        {
            
            //Calculate closest mine
            switch(ovride)
            {
                case "BaseBuild":
                    
                    BuildBuilding(UnitType.BASE, true);
                    break;
                case "BarrackBuild":
					if (myBarracks.Count < maxBarracks)
						BuildBuilding(UnitType.BARRACKS);
                    break;
                case "GatherGold":
					int closeMine1 = -1;
					if (myWorkers.Count > 0)
					{
						closeMine1 = FindClosestUnit(myWorkers[0], mines);
					}                    

					Unit myMine1 = GameManager.Instance.GetUnit(closeMine1);
					Unit myBase1 = GameManager.Instance.GetUnit(mainBaseNbr);
					foreach (int workerNum in myWorkers)
					{
						Unit worker = GameManager.Instance.GetUnit(workerNum);
						if (worker != null && worker.CurrentAction != UnitAction.IDLE)
						{
							continue;
						}

						Gather(worker, myMine1, myBase1);
					}
                    break;
                case "Refine":
					BuildBuilding(UnitType.REFINERY);
                    break;
                case "Worker":
                    Unit myBase2 = GameManager.Instance.GetUnit(mainBaseNbr);
                    if (myBase2 != null && myBase2.IsBuilt && myBase2.CurrentAction == UnitAction.IDLE)
                    {
                        Train(myBase2, UnitType.WORKER);
                    }
                    break;
				case "":
                    Debug.LogWarning("No override given");
                    break;
			}
            

            int closeMine = -1;
            if(myWorkers.Count > 0)
            {
				closeMine = FindClosestUnit(myWorkers[0], mines);
			}
            
            //If there's a valid closest mine 
            if(myBases.Count == 0)
            {
				BuildBuilding(UnitType.BASE, true);
			}
            if( myBases.Count > 0)
            {
                mainBaseNbr = myBases[0];
            }
            else
            {
                mainBaseNbr = -1;
            }
            if (myBarracks.Count < maxBarracks)
            {
                BuildBuilding(UnitType.BARRACKS);
            }
            if (myRefineries.Count < maxRefineries)
            {
                BuildBuilding(UnitType.REFINERY);
            }
            if (myWorkers.Count < maxWorkerCount)
            {
                foreach (int baseNum in myBases)
                {
                    Unit unit = GameManager.Instance.GetUnit(baseNum);
                    if (unit != null && unit.CurrentAction == UnitAction.IDLE && Gold >= Constants.COST[UnitType.WORKER] && myWorkers.Count < 20)
                    {
                        Train(unit, UnitType.WORKER);
                    }
                }
            }
			Unit myMine = GameManager.Instance.GetUnit(closeMine);
            Unit myBase = GameManager.Instance.GetUnit(mainBaseNbr);
			foreach (int workerNum in myWorkers)
            {
                Unit worker = GameManager.Instance.GetUnit(workerNum);
                if(worker != null && worker.CurrentAction != UnitAction.IDLE)
                {
                    continue;
                }

                Gather(worker, myMine, myBase);
            }
        }

        private void GatherGold()
        {
			int closeMine = -1;
			if (myWorkers.Count > 0)
			{
				closeMine = FindClosestUnit(myWorkers[0], mines);
			}

			Unit myMine = GameManager.Instance.GetUnit(closeMine);
			Unit myBase = GameManager.Instance.GetUnit(mainBaseNbr);
			foreach (int workerNum in myWorkers)
			{
				Unit worker = GameManager.Instance.GetUnit(workerNum);
				if (worker != null && worker.CurrentAction != UnitAction.IDLE)
				{
					continue;
				}

				Gather(worker, myMine, myBase);
			}
		}

        private void BuildArmy()
        {
            if (mySoldiers.Count < maxSoldierCount)
            {
                foreach (int barracks in myBarracks)
                {
                    Unit barrack = GameManager.Instance.GetUnit(barracks);
                    if (barrack != null && barrack.IsBuilt && barrack.CurrentAction == UnitAction.IDLE)
                    {
                        float val = (float)mySoldiers.Count / (float)myArchers.Count;
                        //ensure we have 2x archers to soldiers
                        if (val < 2)
                        {
                            Train(barrack, UnitType.ARCHER);
                        }
                        else
                        {
                            Train(barrack, UnitType.SOLDIER);
                        }
                    }
                }
            }
        }

        private void Attack()
        {
            AttackEnemy(mySoldiers);
            AttackEnemy(myArchers);
        }

        
        #endregion
    }
}