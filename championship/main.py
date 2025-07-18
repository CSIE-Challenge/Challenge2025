import json
import os
import random
import copy

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "config.json")) as f:
    config = json.loads(f.read())
    for i in config["players"]:
        i["agent-script"] = os.path.join(config["agent_dir_path"], i["agent-script"])

match_config = {
    "title": config["title"],
    "python-interpreter": config["python_interpreter_path"],
    "nw": {},
    "ne": {},
    "sw": {},
    "se": {},
}

round_names = [
    "round-1-1.json",
    "round-1-2.json",
    "round-1-3.json",
    "round-1-4.json",
    "round-1-5.json",
    "round-2-1.json",
    "round-2-2.json",
    "round-2-3.json",
    "round-2-4.json",
    "round-2-5.json",
    "round-3-1.json",
    "round-3-2.json",
]



# wins, loses, score diff, team id
total_scores = [[0, 0, 0, i] for i in range(10)]
scores_history = [total_scores]
ranks_history = [[i for i in range(10)]]

round_id = 0
while round_id < 11:
    result_path = os.path.join(
        script_dir, "match-data", f"result-{round_names[round_id]}"
    )
    if not os.path.exists(result_path):
        break
    scores = [[j for j in i] for i in total_scores]
    with open(result_path) as f:
        result_dict = json.loads(f.read())
        for i in result_dict:
            team_id = int(i) - 1
            scores[team_id][0] -= result_dict[i]["win"]
            scores[team_id][1] += result_dict[i]["lose"]
            scores[team_id][2] -= result_dict[i]["score_diff"]
    total_scores = scores
    scores_history.append([[j for j in i] for i in total_scores])
    scores = sorted(total_scores)
    ranks_history.append([i[3] for i in scores])
    round_id += 1


def inject_token(orig_path, prefix, old_token, new_token) -> str:
    directory = os.path.dirname(orig_path)
    filename = os.path.basename(orig_path)
    new_path = os.path.join(directory, prefix + filename)
    with open(orig_path) as f:
        body = f.read()
    with open(new_path, "w") as f:
        f.write(body.replace(old_token, new_token))
    return new_path


if round_id == 10:
    # championship
    team1, team2 = ranks_history[9][0], ranks_history[9][1]
    maps = random.sample(config["maps"], 4)
    for i in range(4):
        key = ["nw", "ne", "sw", "se"][i]

        token = "a" + str(i) * 7
        match_config[key]["player-left"] = copy.deepcopy(config["players"][team1])
        match_config[key]["player-left"]["agent-script"] = inject_token(
            match_config[key]["player-left"]["agent-script"],
            key,
            match_config[key]["player-left"]["token"],
            token,
        )
        match_config[key]["player-left"]["token"] = token

        token = "b" + str(i) * 7
        match_config[key]["player-right"] = copy.deepcopy(config["players"][team2])
        match_config[key]["player-right"]["agent-script"] = inject_token(
            match_config[key]["player-right"]["agent-script"],
            key,
            match_config[key]["player-right"]["token"],
            token,
        )
        match_config[key]["player-right"]["token"] = token

        match_config[key]["map"] = maps[0]
        maps = maps[1:]
elif round_id == 11:
    team1, team2 = ranks_history[9][0], ranks_history[9][1]
    match_config["nw"]["player-left"] = config["players"][team1]
    match_config["nw"]["player-right"] = config["players"][team2]
    match_config["nw"]["map"] = config["tie_breaker_map"]
    match_config.pop("ne")
    match_config.pop("sw")
    match_config.pop("se")
else:
    # get omitted teams
    if round_id < 5:
        no_team1, no_team2 = ranks_history[0][round_id * 2 : round_id * 2 + 2]
    else:
        no_team1, no_team2 = ranks_history[5][
            (round_id - 5) * 2 : (round_id - 5) * 2 + 2
        ]
    all_teams = []
    for i in range(10):
        j = ranks_history[round_id][i]
        if j not in [no_team1, no_team2]:
            all_teams.append(j)
    for i in range(4):
        key = ["nw", "ne", "sw", "se"][i]
        match_config[key]["player-left"] = config["players"][all_teams[i * 2]]
        match_config[key]["player-right"] = config["players"][all_teams[i * 2 + 1]]
        match_config[key]["map"] = random.choice(config["maps"])

config_path = os.path.join(script_dir, "match-data", round_names[round_id])
with open(config_path, "w") as f:
    f.write(json.dumps(match_config, indent=2))
