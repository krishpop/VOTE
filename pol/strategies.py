import operator

"""
      As of 9/25/90

      0   Popular decision                        [A]  @@@(POPULAR)
      1   Inconsistent constituency               [B]  @@@(INCONSISTENT-CONSTITUENCY)
      2   Non-partisan decision                   [B]  @@@(NON-PARTISAN)
      3   Not constitutional                      [B]  @@@(NOT-CONSTITUTIONAL)
      4   Unimportant Bill                        [B]  @@@(UNIMPORTANT-BILL)
      5   Balance the books                       [C]  @@@(BALANCE-THE-BOOKS)
      6   Best for the country                    [C]  @@@(BEST-FOR-THE-COUNTRY)
      7   Minimize adverse effects                [C]  @@@(MINIMIZE-ADVERSE-EFFECTS)
      8   Not good enough                         [C]  @@@(NOT-GOOD-ENOUGH)
      9   Partisan Decision                       [C]  @@@(PARTISAN)
      10  Shifting alliances                      [C]  @@@(SHIFTING-ALLIANCES)
      11  Simple consensus                        [C]  @@@(SIMPLE-CONSENSUS)
      12  Normative decision                      [D]  @@@(NORMATIVE)
      13  Simple Majority                         [D]  @@@(SIMPLE-MAJORITY MAJORITY)
  *   14  Deeper analysis                         [E]  @  (DEEPER-ANALYSIS)
      15  No decision                             [F]  @ @(NO-DECISION)
      16  Change of heart                         [X]  @@@(CHANGE-OF-HEART)
      17  Innoculation                            [X]  @@@(INNOCULATION)
      18  It couldn't pass                        [X]  @@@(IT-COULD-NOT-PASS)
      19  Mixed constituency                      [X]   @@(MIXED-CONSTITUENCY)
      20  Unpopular decision                      [X]   @@(UNPOPULAR)

"""

def flatten(a_list):
    return [item for sublist in a_list for item in sublist]

# ------------------------------------------------------------------
#  firm-decision  sets final outcome of decision structure
# ------------------------------------------------------------------

def firm_decision(decision, side, reasons, old_downside, strat):
    bill = DBBill.getById(decision.bill)
    filter_fin = lambda stance : stance.source == bill.id
    downside = filter(filter_fun, flatten(old_downside))
    record = collect_bills(downside)
    
    decision.result = side
    decision.reason = reasons
    decision.strategy = strat
    
    if record:
        decision.downside_record = record
        decision.downside = remove_intersection(downside, record, operator.eq)
    
    else:
        decision.downside = downside

    return decision

def set_decision_outcome(decision, result, strat):
    if result == "FOR":
        reason = decision.for_stances
        dowside = decision.agn_stances
    elif result == "AGN":
        reason = decision.agn_stances
        downside = decision.for_stances
    else:
        print "Reason expected to be FOR or AGN. Got: %s" % reason
        return
    
    return firm_dicision(decision, result, reason, downside, strat)

"""
==================================================================
      0   Popular decision                        [A] @(POPULAR)

  Remarks:       Vote is consistent with major constituencies.
  Quote:         I just try to vote my district.
                 I was sent to Washington to represent the way people back home feel.
                 This is what the vast majority want.
                 I owe it to my constiuents if they feel that strongly about it. [Delegate stance]
  Rank:          "A"
  Test:          All stances on one side of bill.
  Test-code:     STRAT-POPULAR
  Example:       (VOTE 'BRUCE 'PLANT-CLOSING)
==================================================================
"""    

def strat_popular(decision, strat):
    for_stances = decision.for_Stances
    agn_stances = decision.agn_stances
    
    if not for_stances and agn_stances:
        return firm_decision(decision, "AGN", agn_stances, [], strat)
    elif not agn_stances and for_stances:
        return firm_decision(decision, "FOR", for_stances, [], strat)
    else:
        return None


"""
==================================================================
      1   Inconsistent constituency               [B] @(INCONSISTENT-CONSTITUENCY)
    Same group on both sides of issue
==================================================================
"""

def strat_inconsistent_constituency(decision, strat):
    source_conflicts = decision.split_group
    result = consensus(decision)
    
    if not source_conflicts:
        return None
    elif result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

def majority(decision):
    fors = decision.number_for
    agns = decision.number_agn
    
    if fors > agns:
        return "FOR"
    elif agns > fors:
        return "AGN"
    else:
        return None

def consensus(decision)
    filter_fun = lambda lst : lst[0]
    MI = map(filter_fun, collect_MI(decision))
    
    if len(remove_duplicates(MI)) == 1 :
        return MI[0]
    else:
        return None

def collect_MI(decion):
    result = [decision.MI_stance, decision.MI_group, decision.MI_credo, decision.MI_record, decision.MI_norm]
    
    filter_fun = lambda x : x != []
    return filter(filter_fun, result)


"""
==================================================================
      2   Non-partisan decision                   [B]  (NON-PARTISAN)
  
  Remarks:       Vote of conscience or credo that violates party line.  Not a district vote.
  Quote:         Sometimes party loyalty demands too much. (JFK)
  Rank:          "B"
  Test:          Major conflict between credo and party stances.
==================================================================
"""
#  The vote is a matter of conscience.
#  The credo position is in conflict with a party position.
#  The credo position is very important.

def strat_non_partisan(decision, strat):
    member = DBMember.getById(decision.member)

    credo = decision.MI_credo
    credo_side = credo[0]
    credo_stance_list = credo[1]
    opposing_groups = decision.group_agn if credo_side == "FOR" else decision.group_for
    
    party = "Unknown Party Affiliation"
    if member.party == "REP":
        party = "REPUBLICANS"
    if member.party == "DEM":
        party = "Democrats"
    
    # Translate the following and add it to the if statement
    # below:

    # (member party (mapcar #'stance-source opposing-groups)
    #any(party == group.stance for group)
    
    credo_stance1 = DBStance.getById(credo_stance_list[0])
    
    if (credo and opposing_groups and credo_stance_list and
        most_important?(credo_stance1.importance):
        return set_decision_outcome(decision, credo_side, strat)
    else:
        return None

"""
==================================================================
      3   Not constitutional                      [B]  (NOT-CONSTITUTIONAL)

  Remarks:       Vote against a measure that would be struck down by
                 the Supreme Court.
  Rank:          "B"
==================================================================
"""

def strat_not_constitutional(decision, strat):
    constitution_issue = DBIssue.getByName("CONSTITUTION")
    filter_fun = lambda stance : DBStance.getById(stance).issue == constitution_issue

    result = consensus(decision)

    if result == "AGN" and filter(filter_fun, decision.agn_stances):    
    
        reason = decision.agn_stances
        downside = decision.for_stances
        return firm_decision(decision, result, reason, downside, strat)
    
    else:
        return None
    
"""
==================================================================
      4   Unimportant Bill                        [B]   (UNIMPORTANT-BILL)
  
  Date-open:     Monday, May 22, 1989
  Symbol:        STRATEGY.681
  Name:          "Unimportant Bill"
  Sort-key:      "BUnimportant Bill"
  Synonyms:      (UNIMPORTANT-BILL)
  Isa-depth:     ""
  Remarks:       Not much riding on this bill.
  
  Quote:         [Morrison:] some things that are close calls are not treated
                 as close calls because they're not important enough.  I mean
                 its very different if there's enough riding -- either substantively
                 or politically -- on a vote.  You might have exactly the same
                 tensions among the various priorities if you were to pull 
                 this up, but it might be about how you spend $100,000 and you
                 say, **** this.
  
  Rank:          "B"
  Test:          Importance of bill is minimal.
==================================================================
"""

def strat_unimportant_bill(decision, strat):
    result = consensus(decision)
    importance = DBBill.GetById(decision.bill).importance
    
    if result and importance == "C":
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      5   Balance the books                       [C]  (BALANCE-THE-BOOKS)

  Remarks:       Offset current vote with past or future votes.
  Quote:         I know you are upset with this vote, but I have always been there in the
                   past, and I shall be there in the future.
                 I will make it up to you.
                 (point to specific past votes)
  Rank:          "C"
==================================================================
"""

def strat_balance_the_books(decision, strat):
    result = majority(decision)
    split  = decision.split_record
    if result and split:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      6   Best for the country                    [C]  (BEST-FOR-THE-COUNTRY)

  Remarks:       Take the broad view, over parochial interests.
  Quote:         The needs of the country, in this case, must come first.
  Rank:          "C"
  Test:          National interest in conflict with local interest.
==================================================================
"""

# relies on a group: country which has the broad issue agenda for
#  the whole country.  Each congressman has a positive relation with COUNTRY.

def strat_best_for_country(decision, strat):
    result = consensus(decision)
    country = DBGroup.GetByName("COUNTRY")

    # Translate the following once you know more about group_for.
    # Is it a stance object or group object?

    #(country-for (collect (decision-group-for decision)
                              #'(lambda (st) (eq country (reveal-source st)))))
    country_for = None
    # (country-agn (collect (decision-group-agn decision)
                              #'(lambda (st) (eq country (reveal-source st))))) 
    country_agn = None
    
    if result == "FOR" and country_for and not country_agn:
        return set_decision_outcome(decision, result, strat)
    elif result == "AGN" and country_agn and not country_for:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      7   Change of heart                         [C]  (CHANGE-OF-HEART)
  
  Remarks:       Reverse a credo/vote position on the record to accomodate
                 conflict in constituencies.
  Quote:         A foolish consistency is the hobgoblin of small minds.
  Rank:          "C"
  Test:          Credo importance is less than conflicting relation importance.
==================================================================
"""

def strat_change_of_heart(decision, strat):
    result = majority(decision)
    split  = decision.split_credo
    if result and split:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      8   Inoculation                            [C]  (INOCULATION)
  
  Remarks:       Decision which may prove to be unpopular later on.
                 Need to begin laying groundwork for defense early on.
  Rank:          "C"
  Test:          Low priority stances, pro or con.
==================================================================
"""

def strat_inoculation(decision, strat):
    result = majority(decision)
    split_groups = decision.group_for and decision.group_agn
    importance_level = None
    # SAME ISSUE AS ABOVE. Check whether group_for is stances
    # or groups. Otherwise, stance-importance not defined.
    if split_groups:
        temp = decision.group_for + decision.group_agn
        temp.sort(key=lambda stance: stance.importance)
        importance_level = temp[0].importance
        
     if result and split_groups and less_than_importance?(importance_level1, "B"):
        return set_decision_outcome(decision, result, strat)
     else:
        return None

"""
==================================================================
      9   It couldn't pass                        [C]  (IT-COULD-NOT-PASS)

  Remarks:       Do not waste a vote on a symbolic measure.  Better to
                 build credibility and a consensus for the future.
  Quote:         Why waste a vote on a measure that has so little chance of passing.
  Rank:          "C"
  Test:          Bill has far higher importance (and low likelihood of passage)
                 but for issue stance consistent (but stronger than) with my own.
                 This is the flip side of not-good-enough.
==================================================================
"""

def strat_could_not_pass(decision, strat)
    result = majority(decision)
    billid = decision.bill
    if result == "AGN" and could_not_pass?(billid):
        return set_decision_outcome(decision, result, strat)
    else:
        return None

def might_pass?(billid):
    tally = DBBill.GetById(billid).vote_tally
    
    if tally:
        return approved?(billid) or vote_ratio(billid) > 1

def could_not_pass?(billid):
    tally = DBBill.GetById(billid).vote_tally
    if tally:
        return vote_ratio(billid) < 1

def vote_ratio(billid):
    tally = DBBill.GetById(billid).vote_tally
    fors = tally[0]
    agns = tally[1]
    
    if type(fors) != type(0) and type(agns) != type(0):
        return None
    
    # Simply let the ratio be fors if agn is 0 to avoid divide
    # by 0.
    if agn == 0:
        return fors
    
    if fors and agns:
        return fors/agns

def approved?(bill):
    tally = DBBill.GetById(billid).vote_tally
    return tally[0] in ["PASSED", "ADOPTED", "APPROVED"]

def rejected?(bill):
    tally = DBBill.GetById(billid).vote_tally
    return tally[0] in ["REJECTED", "FAILED"]

"""
==================================================================
      10  Minimize adverse effects                [C]  (MINIMIZE-ADVERSE-EFFECTS)

  Remarks:       Adverse effects are less important than the benefits of the vote.
  Quote:         Nothing's perfect.  You have to break a few eggs to make
                 omelets.
  Rank:          "C"
  Test:          The downside results are lower in importance than the upside.
==================================================================
"""

def strat_minimize_adverse_effects(decision, strat):
    result = majority(decision)
    if result:
        MI_up_level = get_MI_level(decision, result)
        MI_down_level = get_MI_level(decision, oposite_result(result))
        if greater_than_importance?(MI_up_level, MI_down_level):
            return set_decision_outcome(decision, result, strat)        
        
    return None

def get_MI_level(decision, result):
    stances = None 
    if result == "FOR":
        stances = decision.for_stances 
    if result == "AGN"
        stances = decision.agn_stances
    
    if stances:
        stances.sort(key=lambda stance: stance.importance)
        return stances[0].importance
     else:
        return "D"

"""
==================================================================
      11  Mixed constituency                      [C]  (MIXED-CONSTITUENCY)

  Remarks:       E.g., rural/urban. can justify pro-rural vote to urbans by
                 pointing to other constituency, and vice-versa.
  Rank:          "C"
  Test:          District must be divided and there should be symmetry on stances.
==================================================================
"""

# note - same as balance the books ...


"""
==================================================================
      12  Not good enough                         [C]  (NOT-GOOD-ENOUGH)

  Remarks:       Bill importance is less than my own stances would call for.
                 For example, personal stance of A, bill importance of C.
  Quote:         I would have voted for a stronger bill.
                 This measure is a fraud.  It has no teeth in it.
  Rank:          "C"
  Test:          Compare importance of bill stance with own stances.  Check for disparity.
==================================================================
"""

def strat_not_good_enough(decision, strat):

    result = majority(decision)
    MI_up_level = None
    MI_bill_level = None
    if result:
        MI_up_level = get_MI_level(decision, result)
        MI_bill_level = get-MI-bill-level(decision, result)
    
    if result == "FOR" and greater_than_importance?(MI_up_level, MI_bill_level):
        return set_decision_outcome(decision, "AGN", strat)
    else:
        return None

def get_MI_bill_level(decision, result):
    bill = DBBill.GetById(decision.bill)
    stances = None
    if result == "FOR":
        stances = bill.stance_for
    if result = "AGN":
        stances = bill.stance_agn
     
     if stances:
        stances.sort(key=lambda stance: stance.importance)
        return stances[0].importance
     else:
        # In Python, "A" > None, but we want A to be of
        # higher importance. Hence, we use an importance
        # of "Z" that will be lower than all others.
        return "Z"

"""
==================================================================
      14  Shifting alliances                      [C]  (SHIFTING-ALLIANCES)

  Remarks:       Conflict resolution through changing relations.
                 When two constituencies are in conflict, try to see if one is more
                 valuable or compatible than the other.  If so, shift their relative
                 importance by either lowering one or raising the other.
  Quote:         I am voting with my good friends in ().  I am sorry to disappoint
                 my many supporters in ().  They know that I have fought many fights
                 with them.
  Rank:          "C"
  Test:          Two constituencies in conflict.
                 Identify other important issue in which they disagree which is
                 important to me.  Pick the one that sides with me.
==================================================================
"""

def strat_shifting_alliances(decision, strat):
    result = divided_groups(decision)
    if result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
        15  Simple consensus                        [C] @ (SIMPLE-CONSENSUS)
  
  Status:        "Active"
  Date-open:     Thursday, May 11, 1989
  Symbol:        STRATEGY.1018
  Name:          "Simple consensus"
  Sort-key:      "CSimple consensus"
  Synonyms:      (SIMPLE-CONSENSUS)
  Isa-depth:     ""
  Remarks:       The most important issues/groups/norms etc. concur.
  
  Rank:          "C"
  Test:          Check all most important features
  
  Test-code:     STRAT-SIMPLE-CONSENSUS
==================================================================
"""

def strat_stimple_consensus(decision, strat):
    result = consensus(decision)
    if result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None


