import requests
import json
from concurrent.futures import ThreadPoolExecutor
import concurrent
import chess

http = requests.session()
http.headers.update({"Content-Type": "application/json"})
data = json.dumps({"type": "rated"})

def scrape(http,data):
	res = http.post("https://chessblunders.org/api/blunder/get", data=data)
	puzzle_json = res.json()["data"]
	fen_before = puzzle_json["fenBefore"]
	board = chess.Board(fen_before)
	blunder_move = puzzle_json["blunderMove"]
	board.push_san(blunder_move)
	fen_after = board.fen()
	elo = puzzle_json["elo"]

	forced_line = ",".join(puzzle_json["forcedLine"])
	print("{}|{}|{}".format(fen_after,forced_line,elo))
	return True


with ThreadPoolExecutor(max_workers=40) as executor:
    processes = [executor.submit(scrape, http, data) for i in range(10)]
    for future in concurrent.futures.as_completed(processes):
    	future.result()


