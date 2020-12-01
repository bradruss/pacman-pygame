In order to create a new level for our pacman game you will need to RUN levelCreator.py

****GENERAL INFO*****
By default, corridors will have a width (or height) of 50 depending on if it is vertical or horizontal
The corridor that you must start with is a horintal corridor in the middle of the map. For proper implementation start
with (g, H,350,850,250,250). This will provide you with a great position to build out with.
The format to create a new corridor is as follows ("name of corridor", type(H or V), xStart, xEnd, yStart,yEnd)
The game board is 1200 units wide, and 600 units tall



*****CREATING HORIZONTAL CORRIDRS******
To create a horizontal corridor, you will need the second argument to be "H". When creating a horizontal corridor the y positions will be the same for both arguments (the y position of the corridor does not change.
EXAMPLE: (g,H,350,850,250,250).


*****CREATING VERTICAL CORRIDORS*********
To create a vertical corridor the second argument must be “V”. When creating a vertical corridor the two x parameters will remain the same.
Example: a,V,350,350,250,550



*****JOINING CORRIDORS ****
Before joining a two corridors, be sure they intersect and form a square at the intersection at the end of both corridors. The format for joining corridors is (join, name of horiz corridor,name of vertical corridor, type of join)
The types of join calls or bl,tl,br,and tr. These correspond to a bottom left join, top left join, bottom right join and top right join.

Example:
(a,V,0,0,0,600) : Vertical corridor that runs the length of the left side of the game board
(b,H,0,1200,0,0) : horizontal corridor that runs the length of the top of the game board
(join,b,a,tl) : This will joing the two corridors at the top left part of the map

***DELETING A CORRIDOR***
To delete a corridor make the call (del, name of corridor)

****UNDOING THE LAST CALL****
To undo the last call that you made type(revert,now)

*****WHEN YOU ARE DONE MAKING A MAP***
When you are done with your map type (done,filename)
*FileName will be the file you write the completed map to

*****LAODING IN AN EXISITNG MAP*****
To load in an existing map for editing tyoe (read_file,filename)
*Filename is the name of the file that you have saved the call to create a prior map in




