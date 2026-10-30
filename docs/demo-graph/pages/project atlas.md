status:: in progress
tags:: work, maps

- A small offline map viewer for hiking trails.
- ## Milestones
	- DONE Tile cache
	- DOING Offline search
	- TODO Export routes as GPX
- ## Open questions
	- Which projection for the overview map?
	- Do we bundle elevation data, or fetch it on first launch?
- ```bash
  atlas build --release
  atlas serve --port 8080
  ```
