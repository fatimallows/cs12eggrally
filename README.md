# cs12eggrally



// const EggUtils = {
//   top: (egg: Egg) => egg.y + egg.height ,
//   bottom: (egg: Egg) => egg.y,
//   left: (egg: Egg) => egg.x ,
//   right: (egg: Egg) => egg.x + egg.width ,
//   updateInModel: (model: Model, updates: Partial<Egg>) =>
//     Model.make({
//       ...model,
//       egg: Egg.make({
//         ...model.egg,
//         ...updates,
//       }),
//     }),
// } 

// const EggnemiesUtils = {
//   top: (eggnemies: Eggnemies) => eggnemies.y + eggnemies.height ,
//   bottom: (eggnemies: Eggnemies) => eggnemies.y,
//   left: (eggnemies: Eggnemies) => eggnemies.x ,
//   right: (eggnemies: Eggnemies) => eggnemies.x + eggnemies.width ,
//   updateInModel: (model: Model, updates: Partial<Egg>) =>
//     Model.make({
//       ...model,
//       egg: Egg.make({
//         ...model.egg,
//         ...updates,
//       }),
//     }),
// } 

// type Config = typeof Config.Type
// const Config = S.Struct({ //game window
//   worldWidth: S.Number,
//   worldHeight: S.Number, 
//   fps: S.Number,
//   initialHP: S.Number,
//   eggWidth: S.Number,
//   eggHeight: S.Number,
//   eggnemiesWidth: S.Number,
//   eggnemiesHeight: S.Number,
//   eggnemiesCount: S.Number,
//   velocity: S.Number,
// })

// type Egg = typeof Egg.Type
// const Egg = S.Struct({
//   x: S.Number,
//   y: S.Number,
//   width: S.Number,
//   height: S.Number,
//   hp: S.Number,
//   vx: S.Number,
//   vy: S.Number,
// })

// type Eggnemies = typeof Eggnemies.Type
// const Eggnemies = S.Struct({
//   x: S.Number,
//   y: S.Number,
//   width: S.Number,
//   height: S.Number,
//   vx: S.Number,
//   vy: S.Number,
//   id: S.Number,
// })

// type Model = typeof Model.Type
// const Model = S.Struct({
//   config: Config,
//   egg: Egg,
//   eggnemies: S.Array(Eggnemies),
//   isGameOver: S.Boolean,
//   score: S.Number,
//   ticks: S.Number,
// })

// const initModel = pipe(
//   Model.make({
//     config: Config.make({
//       worldWidth: 400,
//       worldHeight: 700,
//       fps: 30,
//       initialHP: 10,
//       eggWidth: 40,
//       eggHeight: 80,
//       eggnemiesWidth: 40,
//       eggnemiesHeight: 80,
//       eggnemiesCount: 10,
//       velocity: 2,
//     }),
//     egg: Egg.make({
//       x: 0,
//       y: 0,
//       width: 40,
//       height: 80,
//       hp: 10,
//       vx: 0,
//       vy: 0,
//     }),
//     isGameOver: false,
//     score: 0,
//     eggnemies: pipe([1,2,3,4,5,6,7,8,9,10], Array.map((eggnemy)=>
//       Eggnemies.make({
//         x: Math.random() * 400,
//         y: Math.random() * 700,
//         width: 40,
//         height: 80,
//         vx: Math.random() * 2 - 1, 
//         vy: Math.random() * 2 - 1, 
//         id: eggnemy,
//       }))
//     ),
//     ticks: 0,
//   }),
//   (model) =>
//     EggUtils.updateInModel(model, {
//       x: model.config.worldWidth / 2,
//       y: model.config.worldHeight / 2,
//     }),
// )

// type Msg = CanvasMsg

// const update = (msg: Msg, model: Model) =>
//   Match.value(msg).pipe(
//     Match.tag("Canvas.MsgKeyDown", ({ key }) =>
//       key.toLowerCase() === "w" && !model.isGameOver ?
//         EggUtils.updateInModel(model, {
//             vy: model.config.velocity,
//           })
//       : key.toLowerCase() === "s" && !model.isGameOver ?
//         EggUtils.updateInModel(model, {
//               vy: -model.config.velocity,
//             })
//       : key.toLowerCase() === "a" && !model.isGameOver ?
//         EggUtils.updateInModel(model, {
//               vx: -model.config.velocity,
//             })
//       : key.toLowerCase() === "d" && !model.isGameOver ?
//         EggUtils.updateInModel(model, {
//               vx: model.config.velocity,
//             })
//       : key === "r" ? initModel
//       : model,
//     ),
//     Match.tag("Canvas.MsgTick", () =>
//       model.isGameOver ? model : (
//         pipe(
//           model, //
//           updateEgg,
//           updateCollision,
//           updateGameOver,
//           updateTicks,
//         )
//       ),
//     ),
//     Match.orElse(() => model),
//   )

// const updateEggnemies = (model: Model): Model =>
//   Model.make({
//     ...model, 
//     eggnemies: model.eggnemies.map(e =>
//       Eggnemies.make({
//         ...e,
//         x: e.x + e.vx,
//         y: e.y + e.vy,
//       })
//     ),
//   })

// const updateCollision = (model: Model): Model => {
//   const egg = model.egg

//   const isColliding = (e: Eggnemies) => {
    
//   }

// }

// const updateGameOver = (model: Model): Model =>
//   Model.make({
//     ...model,
//     isGameOver: true
//   })

// const updateTicks = (model: Model): Model =>
//   Model.make({
//     ...model,
//     ticks: model.ticks + 1,
//   })

// const updateEgg = (model: Model): Model =>
//   EggUtils.updateInModel(model, {
//     x: model.egg.x + model.egg.vx,
//     y: model.egg.y + model.egg.vy,
//   })
  
