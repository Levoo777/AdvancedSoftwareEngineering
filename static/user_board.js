const blocks_object =  {
  "1": 0,
  "2": [
    [
      "green",
      "green"
    ]
  ],
  "3": [
    [
      "green",
      "green"
    ],
    [
      null,
      "green"
    ]
  ],
  "4": [
    [
      "green",
      "green",
      "green"
    ]
  ],
  "5": [
    [
      "green",
      "green",
      "green",
      "green"
    ]
  ],
  "6": [
    [
      null,
      null,
      "green"
    ],
    [
      "green",
      "green",
      "green"
    ]
  ],
  "7": [
    [
      "green",
      "green",
      null
    ],
    [
      null,
      "green",
      "green"
    ]
  ],
  "8": [
    [
      "green",
      "green"
    ],
    [
      "green",
      "green"
    ]
  ],
  "9": [
    [
      null,
      "green",
      null
    ],
    [
      "green",
      "green",
      "green"
    ]
  ],
  "10": [
    [
      null,
      "green",
      "green"
    ],
    [
      "green",
      "green",
      null
    ],
    [
      null,
      "green",
      null
    ]
  ],
  "11": [
    [
      "green",
      "green",
      "green",
      "green",
      "green"
    ]
  ],
  "12": [
    [
      "green",
      "green",
      "green",
      "green"
    ],
    [
      null,
      null,
      null,
      "green"
    ]
  ],
  "13": [
    [
      "green",
      "green",
      "green",
      null
    ],
    [
      null,
      null,
      "green",
      "green"
    ]
  ],
  "14": [
    [
      "green",
      "green",
      "green"
    ],
    [
      null,
      "green",
      "green"
    ]
  ],
  "15": [
    [
      "green",
      "green",
      "green"
    ],
    [
      null,
      "green",
      null
    ],
    [
      null,
      "green",
      null
    ]
  ],
  "16": [
    [
      "green",
      "green",
      "green"
    ],
    [
      "green",
      null,
      "green"
    ]
  ],
  "17": [
    [
      "green",
      "green",
      "green"
    ],
    [
      null,
      null,
      "green"
    ],
    [
      null,
      null,
      "green"
    ]
  ],
  "18": [
    [
      null,
      null,
      "green"
    ],
    [
      null,
      "green",
      "green"
    ],
    [
      "green",
      "green",
      null
    ]
  ],
  "19": [
    [
      null,
      "green",
      null
    ],
    [
      "green",
      "green",
      "green"
    ],
    [
      null,
      "green",
      null
    ]
  ],
  "20": [
    [
      "green",
      "green",
      "green",
      "green"
    ],
    [
      null,
      null,
      "green",
      null
    ]
  ],
  "21": [
    [
      "green",
      "green",
      null
    ],
    [
      null,
      "green",
      null
    ],
    [
      null,
      "green",
      "green"
    ]
  ]
}

const DEFAULT_BLOCK_GRID = [[false, false, false, false, false], [false, false, false, false, false], [false, false, false, false, false], [false, false, false, false, false], [false, false, false, false, false]]
let BOARD_ARRAY = createBoardMatrix()


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


function createBlock (block) {
  let blockGrid = structuredClone(DEFAULT_BLOCK_GRID)
  let newBlock = blockGrid


  for (let i = 0; i < blockGrid.length; i++) {

      if (block.length <= i) break; 

      if (block == 0) {
        newBlock = blockGrid
      } else {

        for (let j = 0; j < blockGrid[i].length; j++) {

          if (block.length[i] <= j) break; 

          if (block[i][j] != null) {
              newBlock[i][j] = true;

          } /* else if (block[i][j] == "red") {
              newBlock[i][j] = "red";

          } else if (block[i][j] == "blue") {
              newBlock[i][j] = "blue";

          } else if (block[i][j] == "blue") {
              newBlock[i][j] = "blue";
          } */
      }
      }


  }

  return newBlock
}



function createListOfBlocksGrid (blocks_object) {
  let BlocksGrid = []
  let block;

  for (const [key, value] of Object.entries(blocks_object)) {

      block = createBlock(value)
      BlocksGrid.push(block)

  }

  return BlocksGrid
}

console.log(createListOfBlocksGrid(blocks_object))

function renderAllBlocks (blocks_object_update) {
  let current_BOARD_BLOCKS = 0;
  const block_grid_layout = createListOfBlocksGrid(blocks_object_update);
   
      let i = 0;     
  
      for (j in block_grid_layout) {
          console.log(block_grid_layout[j])
          if (i < 35) {
              current_BOARD_BLOCKS = BOARD_BLOCKS1;
  
          } else if (i <= 65) {
              current_BOARD_BLOCKS = BOARD_BLOCKS2;
          } else {
              current_BOARD_BLOCKS = BOARD_BLOCKS3;
          }
          
          if (block_grid_layout[j] == 0) {
            const block = document.createElement("div")
            block.classList.add("no-block");
            block.setAttribute('id', `${j}`);
            block.setAttribute("draggable", "false")
            current_BOARD_BLOCKS.append(block)

          } else {
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
}


renderAllBlocks(blocks_object)


function dragndrop (blocks_object_update) {
  const draggables = document.querySelectorAll(".block")
  const squares = document.querySelectorAll(".square")
  const blocks_array = createListOfBlocksGrid(blocks_object_update)

  draggables.forEach(draggable => {
      draggable.addEventListener("dragstart", () =>{
          draggable.classList.add("dragging")
      })

      // draggable.addEventListener("keydown", (ev) => {
      //     console.log("keydown")
      // })

      draggable.addEventListener("dragend", () => {
          console.log("abgebrochen")
          draggable.classList.remove("dragging")
      })
  })

  draggables.forEach(draggable => {
      draggable.addEventListener("click", e => {
          let i = 0;

          let true_squares = draggable.querySelectorAll(".blocksquare-true")
          true_squares.forEach(true_square => {
              true_square.classList.add("click")
          })

          
          draggable.addEventListener("keydown", (ev) => {
              if (ev === " ") {
                  i = (i+1) % 4
                   draggable.classList.add(`rotate${i}`)
              }
          })
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

          data = {
              "action": "block_insert",
              "y": y,
              "x": x,
              "block": draggingBlockId +1,
              "block_matrix": blocks_array[draggingBlockId]
              }
          socket.emit('user_set_block', data);
      
          
      })
  })

}

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

dragndrop(blocks_object)

function updateGameBoardGrid(currentGrid) {

  for (i in currentGrid) {
      for (j in currentGrid[i])
          if (currentGrid[i][j] == "X") {
              continue;

          } else {
              changeColorGameBoard(i, j, currentGrid[i][j])
           }
  }
}

function updateGameBlocks(updatet_version) {
renderAllBlocks(updatet_version)
}