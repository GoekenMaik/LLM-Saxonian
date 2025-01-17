curl -X POST "http://localhost:8000/v1/completions" \
	-H "Content-Type: application/json" \
	--data '{
		"model": "meta-llama/Llama-3.2-1B",
		"prompt": "De Republiek Sudan is en Staat in Noordoost-Afrika an",
		"max_tokens": 512,
		"temperature": 0.5
	}'
