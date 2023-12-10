const board = document.querySelector('#board');
const colors = ['blue', 'green', 'red', 'yellow'];
const SQUARES_NUMBER = 20*20;

const BLOCKS_OBJECT =  {1: [[true]], 2: [[true,true]], 3: [[true,true],[false,true]], 4: [[true,true,true]], 5: [[true,true,true, true]], 6: [[false, false, true],[true,true,true]], 7: [[true, true, false], [false, true, true]], 8: [[true, true], [true, true]], 9: [[false, true, false], [true, true, true]], 10: [[false, true, true], [true, true, false], [false, true, false]], 11: [[true, true, true, true, true]], 12: [[true, true, true, true], [false, false, false, true]], 13: [[true, true, true, false], [false, false, true, true]], 14: [[true, true, true], [false, true, true]], 15: [[true, true, true], [false, true, false], [false, true, false]], 16: [[true, true, true], [true, false, true]], 17: [[true, true, true], [false, false, true], [false, false, true]], 18: [[false, false, true], [false, true, true], [true, true, false]], 19: [[false, true, false], [true, true, true], [false, true, false]], 20: [[true, true, true, true], [false, false, true, false]], 21: [[true, true, false], [false, true, false], [false, true, true]]}
const DEFAULT_BLOCK_GRID = [[false, false, false, false, false], [false, false, false, false, false], [false, false, false, false, false], [false, false, false, false, false], [false, false, false, false, false]]

let BOARD_ARRAY = createBoardMatrix()
let BLOCKS_ARRAY = createBlockMatrix()
let BLOCKS_IN_DEFAULT_GRID = insertBlocksInDefaultBlockArray()

const BOARD_BLOCKS1 = document.querySelector('#blocks1')
const BOARD_BLOCKS2 = document.querySelector('#blocks2')
const BOARD_BLOCKS3 = document.querySelector('#blocks3')

// creates the game board corresponding array
function createBoardMatrix () {
    let matrix = []
    for (let i = 0; i <= 20-1; i++) {
        matrix.push([false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false])
    }

    return matrix;
}

// renders the game board
function createBoard () {
    for (let i = 0; i < BOARD_ARRAY.length; i++) {
        for (let j = 0; j < BOARD_ARRAY[i].length; j++) {
                    const square = document.createElement('div');
                    square.classList.add(`square`);
                    square.setAttribute('id', `${i},${j}`);
                    board.append(square);
        } 
    }
}

createBoard();

// creates the array in which the game blocks are held
function createBlockMatrix () {
    let matrix = []
    for (let i = 0; i < 63; i++) {
        matrix.push([false, false, false, false])
    }

    return matrix;
}

// renders the grid in which the game blocks are held
function renderAllBlocks () {
    let current_BOARD_BLOCKS = 0;
    const block_grid_layout = createListOfBlocksGrid();
     
        let i = 0;     
    
        for (j in block_grid_layout) {

            if (i < 35) {
                current_BOARD_BLOCKS = BOARD_BLOCKS1;
    
            } else if (i <= 65) {
                current_BOARD_BLOCKS = BOARD_BLOCKS2;
            } else {
                current_BOARD_BLOCKS = BOARD_BLOCKS3;
            }
            

            const block = document.createElement("div")
            block.classList.add("block");
            block.setAttribute('id', `${j}`);
            block.setAttribute("draggable", "true")
            current_BOARD_BLOCKS.append(block)

            for (k in block_grid_layout[j]) {
                
                
                for (l in block_grid_layout[j][k]) {

                    const square = document.createElement("div")

                    if (block_grid_layout[j][k][l] == true) {
                        square.classList.add("blocksquare-true")
                        square.setAttribute("id",  `block y${i}, x${l}`)
                        block.append(square);

                    } else {
                        square.classList.add("blocksquare-false")
                        square.setAttribute("id",  `block y${i}, x${l}`)
                        block.append(square);
                    }
                }
                i++;
            }
        }
}

renderAllBlocks()


// changes the color of one coordinate on the game board
function changeColorGameBoard(y, x, color) {
    let element = document.getElementById(`${y},${x}`)
    element.style.backgroundColor = color;

    element.style.boxShadow = `0 0 2px ${color}, 0 0 10px ${color}`
}

// changes the color of on coordinate on the block placeholder
function changeColorBlockBoard(y, x, color) {
    let element = document.getElementById(`${y},${x}`)
    element.style.backgroundColor = color;

    element.style.boxShadow = `0 0 2px ${color}, 0 0 10px ${color}`
}


// inserts the blocks in the array, where the blocks are held
function insertBlocksInDefaultBlockArray () {

    let listOfBlocksInDefaultGrid = createListOfBlocksGrid()
    let blocksArray = structuredClone(BLOCKS_ARRAY)


    let j = 0
    let k = 0

    for (i in blocksArray) {


        if (i % 3 == 0 && i != 0) j++;
        if (k % 3 == 0 && k != 0) k = 0;
 

            for (l in listOfBlocksInDefaultGrid[j][k]) {

                if (listOfBlocksInDefaultGrid[j][k][l] == true) blocksArray[i][l] = true;
            }

        k++
    } 

    return blocksArray
}


// sets the block and color one the game board
function setBlockGameBoard(y, x, block, color) {

    for (let i = 0; i < block.length; i++) {
        for (let j = 0; j < block[i].length; j++) {
            if (block[i][j] == true) {
                changeColorGameBoard(y+i, x+j, color)

            }
        }
    }
}


// creates a block in the default layout
function createBlock (block) {
    let blockGrid = structuredClone(DEFAULT_BLOCK_GRID)
    let newBlock = blockGrid


    for (let i = 0; i < blockGrid.length; i++) {

        if (block.length <= i) break; 

        for (let j = 0; j < blockGrid[i].length; j++) {

            if (block.length[i] <= j) break; 

            if (block[i][j] == true) {
                newBlock[i][j] = true;
            }
        }
    }

    return newBlock
}

// returns the list of game blocks in the default layout
function createListOfBlocksGrid () {
    let BlocksGrid = []
    let block;
    const BlockMatrix = structuredClone(BLOCKS_OBJECT)

    for (const [key, value] of Object.entries(BlockMatrix)) {

        block = createBlock(value)
        BlocksGrid.push(block)

    }

    return BlocksGrid
}

// drag and drop for the blocks and gameboard
function dragndrop () {
    const draggables = document.querySelectorAll(".block")
    const squares = document.querySelectorAll(".square")
    const blocks_array = createListOfBlocksGrid()
    console.log(blocks_array)

    draggables.forEach(draggable => {
        draggable.addEventListener("dragstart", () =>{
            draggable.classList.add("dragging")
        })

        draggable.addEventListener("dragend", () => {
            draggable.classList.remove("dragging")
        })
    })

    
    
    squares.forEach(square => {
        
        square.addEventListener("dragenter", e => {
            e.preventDefault()
            const draggable = document.querySelector(".dragging")
            const draggingBlockId = Number(draggable.id)
            let yx_array = square.id.split(",")
            let y = Number(yx_array[0])
            let x = Number(yx_array[1])


            let currentBlock = blocks_array[Number(draggingBlockId)]

            for (i in currentBlock) {

                for (j in currentBlock[i]) {

                    if (currentBlock[i][j] == true) {
                        let yi = y+Number(i)
                        let xj = x+Number(j)

                        let trueSquare = document.getElementById(`${yi.toString()},${xj.toString()}`)
                        trueSquare.classList.add("dragenter")
                    } 
                }
            }
            
        })
        

        square.addEventListener("dragleave", e => {
            e.preventDefault()
            const dragEnters = document.querySelectorAll(".dragenter")
            dragEnters.forEach((element) => element.classList.remove("dragenter"))
        })


        square.addEventListener("dragover", e => {
            e.preventDefault()
        })

        square.addEventListener("drop", e => {
            e.preventDefault()
            console.log("drop")
            const draggable = document.querySelector(".dragging")
            const draggingBlockId = Number(draggable.id)

            let yx_array = square.id.split(",")
            let y = Number(yx_array[0])
            let x = Number(yx_array[1])

            setBlockGameBoard(y, x, blocks_array[draggingBlockId], "cyan")
            
        })
    })

}

dragndrop()

// function updateGrid(currentGrid) {
//     for (i in currentGrid) {
//         for (j in currentGrid[i])
//             if (currentGrid[i][j] == "X") {
//                 break;

//             } else {
//                 changeColorGameBoard(i, j, currentGrid[i][j])
//              }
//     }
// }