execute: 
1. batch_split.py
	Split the audio with 5 sec windows to match the input in Path('data/audio'). 
2. batch_draw.py
	Invoke draw.py, extract square frequency maps for all audio clips.
3. statis.py
	Count numbers of each species. For the species with number of samples less than 500, extract un-useful samples manually with recognizable features.
4. calgray.py
	For species with amount of samples above or equal 500, extract samples by calgray.py to move to class none. 

	
