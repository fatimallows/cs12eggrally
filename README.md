# cs12eggrally

// const BirdUtils = {
//   top: (bird: Bird) => bird.y - bird.radius,
//   bottom: (bird: Bird) => bird.y + bird.radius,
//   left: (bird: Bird) => bird.x - bird.radius,
//   right: (bird: Bird) => bird.x + bird.radius,
//   updateInModel: (model: Model, updates: Partial<Bird>) =>
//     Model.make({
//       ...model,
//       bird: Bird.make({
//         ...model.bird,
//         ...updates,
//       }),
//     }),
// } 

// const Config = S.Struct({ // game window (?)
//   screenWidth: S.Int,
//   screenHeight: S.Int,
//   fps: S.Int,
//   canvasId: S.String,
//   jumpY: S.Int,
// })

// type Bird = typeof Bird.Type
// const Bird = S.Struct({
//   x: S.Number,
//   y: S.Number,
//   radius: S.Number,
//   vy: S.Number,
//   ay: S.Number,
// })

// type Rectangle = typeof Rectangle.Type
// const Rectangle = S.Struct({
//   x: S.Number,
//   y: S.Number,
//   width: S.Number,
//   height: S.Number,
// })

// const PipePairUtils = {
//   topPipe: (pair: PipePair): Rectangle =>
//     Rectangle.make({
//       x: pair.x,
//       y: 0,
//       width: pair.pipeWidth,
//       height: pair.holeStartY,
//     }),
//   bottomPipe: (pair: PipePair): Rectangle =>
//     pipe(
//       {
//         y: pair.holeStartY + pair.holeHeight,
//       },
//       ({ y }) =>
//         Rectangle.make({
//           x: pair.x,
//           y,
//           width: pair.pipeWidth,
//           height: pair.screenHeight - y,
//         }),
//     ),
//   centerX: (pair: PipePair) => pair.x + pair.pipeWidth / 2,
// }

// type PipePair = typeof PipePair.Type
// const PipePair = S.Struct({
//   x: S.Number,
//   vx: S.Number,
//   holeStartY: S.Number,
//   holeHeight: S.Number,
//   pipeWidth: S.Number,
//   screenHeight: S.Number,
//   hasBeenPassed: S.Boolean,
// })

// type Model = typeof Model.Type
// const Model = S.Struct({
//   config: Config,
//   bird: Bird,
//   isGameOver: S.Boolean,
//   score: S.Int,
//   ticks: S.Int,
//   pipePairs: S.Array(PipePair),
// })

// const initModel = pipe(
//   Model.make({
//     config: Config.make({
//       screenWidth: 400,
//       screenHeight: 700,
//       fps: 30,
//       canvasId: "canvas",
//       jumpY: -10,
//     }),
//     bird: Bird.make({
//       x: 0,
//       y: 0,
//       radius: 20,
//       vy: 0,
//       ay: 1,
//     }),
//     isGameOver: false,
//     score: 0,
//     ticks: 0,
//     pipePairs: [],
//   }),
//   (model) =>
//     BirdUtils.updateInModel(model, {
//       x: model.config.screenWidth / 2,
//       y: model.config.screenHeight / 2,
//     }),
// )

// type Msg = CanvasMsg

// const update = (msg: Msg, model: Model) =>
//   Match.value(msg).pipe(
//     Match.tag("Canvas.MsgKeyDown", ({ key }) =>
//       key === " " && !model.isGameOver ?
//         {
//           model: BirdUtils.updateInModel(model, {
//             vy: model.config.jumpY,
//           }),
//           cmd: Cmd.ofSub(async () => {
//             const audio = new Audio("resources/jump.wav")
//             audio.play()
//           }),
//         }
//       : key === "r" ? initModel
//       : model,
//     ),
//     Match.tag("Canvas.MsgTick", () =>
//       model.isGameOver ? model : (
//         pipe(
//           model, //
//           updateBird,
//           updateCollision,
//           updateGameOver,
//           updateCreateNewPipePair,
//           updatePipePairs,
//           updateScore,
//           updateTicks,
//         )
//       ),
//     ),
//     Match.orElse(() => model),
//   )

// const isInCollision = (
//   cx: number,
//   cy: number,
//   radius: number,
//   rect: Rectangle,
// ) =>
//   pipe(
//     {
//       testX:
//         cx < rect.x ? rect.x
//         : cx > rect.x + rect.width ? rect.x + rect.width
//         : cx,
//       testY:
//         cy < rect.y ? rect.y
//         : cy > rect.y + rect.height ? rect.y + rect.height
//         : cy,
//     },
//     ({ testX, testY }) =>
//       Math.sqrt((cx - testX) ** 2 + (cy - testY) ** 2) < radius,
//   )

// const didBirdHitAnyPipePair = (model: Model) =>
//   pipe(
//     model.pipePairs,
//     Array.some(
//       (pair) =>
//         isInCollision(
//           model.bird.x,
//           model.bird.y,
//           model.bird.radius,
//           PipePairUtils.topPipe(pair),
//         ) ||
//         isInCollision(
//           model.bird.x,
//           model.bird.y,
//           model.bird.radius,
//           PipePairUtils.bottomPipe(pair),
//         ),
//     ),
//   )

// const updateCollision = (model: Model) =>
//   didBirdHitAnyPipePair(model) ?
//     Model.make({
//       ...model,
//       isGameOver: true,
//     })
//   : model

// const updateTicks = (model: Model) =>
//   Model.make({
//     ...model,
//     ticks: model.ticks + 1,
//   })

// const updateGameOver = (model: Model) =>
//   pipe(
//     model, //
//     ({ bird, config }) =>
//       BirdUtils.bottom(bird) > config.screenHeight || BirdUtils.top(bird) < 0 ?
//         Model.make({
//           ...model,
//           isGameOver: true,
//         })
//       : model,
//   )

// const updateBird = (model: Model) =>
//   BirdUtils.updateInModel(model, {
//     y: model.bird.y + model.bird.vy,
//     vy: model.bird.vy + model.bird.ay,
//   })

// const updateCreateNewPipePair = (model: Model) =>
//   model.ticks % (model.config.fps * 3) === 0 ?
//     Model.make({
//       ...model,
//       pipePairs: pipe(
//         model.pipePairs,
//         Array.append(
//           PipePair.make({
//             x: model.config.screenWidth,
//             vx: -3,
//             holeStartY: Math.floor(
//               Math.random() * (model.config.screenHeight - 200),
//             ),
//             holeHeight: 200,
//             pipeWidth: 100,
//             hasBeenPassed: false,
//             screenHeight: model.config.screenHeight,
//           }),
//         ),
//       ),
//     })
//   : model

// const updatePipePairs = (model: Model) =>
//   Model.make({
//     ...model,
//     pipePairs: pipe(
//       model.pipePairs,
//       Array.map((pair) =>
//         PipePair.make({
//           ...pair,
//           x: pair.x + pair.vx,
//         }),
//       ),
//     ),
//   })

// const updateScore = (oldModel: Model) =>
//   pipe(
//     oldModel.pipePairs,
//     Array.reduce(
//       Model.make({ ...oldModel, pipePairs: [] }),
//       (accModel, pair) =>
//         !pair.hasBeenPassed && PipePairUtils.centerX(pair) <= accModel.bird.x ?
//           Model.make({
//             ...accModel,
//             score: accModel.score + 1,
//             pipePairs: [
//               ...accModel.pipePairs,
//               PipePair.make({
//                 ...pair,
//                 hasBeenPassed: true,
//               }),
//             ],
//           })
//         : Model.make({
//             ...accModel,
//             pipePairs: [...accModel.pipePairs, pair],
//           }),
//     ),
//   )

// const view = (model: Model) =>
//   pipe(
//     model, //
//     ({ config, bird, pipePairs }) => [
//       Canvas.Clear.make({
//         color: "skyblue",
//       }),
//       Canvas.SolidCircle.make({
//         x: bird.x,
//         y: bird.y,
//         color: "red",
//         radius: bird.radius,
//       }),
//       Canvas.CanvasImage.make({
//         x: bird.x - 22,
//         y: bird.y - 22,
//         src: "resources/poring.gif",
//       }),
//       ...viewPipePairs(pipePairs),
//       Canvas.Text.make({
//         x: 20,
//         y: 20,
//         text: `${model.ticks}`,
//         color: "black",
//         fontSize: 12,
//       }),
//       Canvas.Text.make({
//         x: config.screenWidth / 2,
//         y: 50,
//         text: `${model.score}`,
//         color: "black",
//         fontSize: 20,
//       }),
//       viewGameOver(model),
//     ],
//   )

// const viewGameOver = (model: Model) =>
//   model.isGameOver ?
//     Canvas.Text.make({
//       x: config.screenWidth / 2,
//       y: config.screenHeight / 2,
//       text: "GAME OVER",
//       color: "black",
//       fontSize: 20,
//     })
//   : Canvas.NullElement.make()

// const viewPipePairs = (pipePairs: readonly PipePair[]) =>
//   pipe(
//     pipePairs, //
//     Array.map(viewPipePair),
//     Array.flatten,
//   )

// const viewPipePair = (pair: PipePair) => [
//   Canvas.SolidRectangle.make({
//     ...PipePairUtils.topPipe(pair),
//     color: "green",
//   }),
//   Canvas.SolidRectangle.make({
//     ...PipePairUtils.bottomPipe(pair),
//     color: "green",
//   }),
// ]

// const root = document.getElementById("app")!
// const { config } = initModel

// startModelCmd(
//   root,
//   initModel,
//   update,
//   canvasView(
//     config.screenWidth,
//     config.screenHeight,
//     config.fps,
//     config.canvasId,
//     view,
//   ),
// )


