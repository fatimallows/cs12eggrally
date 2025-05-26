import { Array, Schema as S, Match, pipe } from "effect"
import { Cmd, startModelCmd } from "cs12242-mvu/src/index"
import { CanvasMsg, canvasView } from "cs12242-mvu/src/canvas"
import * as Canvas from "cs12242-mvu/src/canvas"

type Rectangle = typeof Rectangle.Type
const Rectangle = S.Struct({
  x: S.Number,
  y: S.Number,
  height: S.Number,
  width: S.Number,
})

const EggUtils = {
  top: (egg: Egg) => egg.y,
  bottom: (egg: Egg) => egg.y + egg.height,
  left:  (egg: Egg) => egg.x,
  right:  (egg: Egg) => egg.x + egg.width,
  updateInModel: (model: Model, updates: Partial<Egg>) =>
    Model.make({
      ...model,
      egg: Egg.make({
        ...model.egg,
        ...updates,
      }),
    }),
} 


const Config = S.Struct({ 
  screenWidth: S.Int,
  screenHeight: S.Int,
  fps: S.Int,
  canvasId: S.String,
  velocity: S.Number,
  maxHp: S.Number,
  eggInvincibilityFrames: S.Int, 
})
type Config = typeof Config.Type


type Egg = typeof Egg.Type
const Egg = S.Struct({
  x: S.Number,
  y: S.Number,
  height: S.Number,
  width: S.Number,
  vx: S.Number,
  vy: S.Number,
  hp: S.Number,
})


type Eggnemies = typeof Eggnemies.Type
const Eggnemies = S.Struct({
  x: S.Number,
  y: S.Number,
  height: S.Number,
  width: S.Number,
  vx: S.Number,
  vy: S.Number,
  id: S.Int,
})

type Model = typeof Model.Type
const Model = S.Struct({
  config: Config,
  egg: Egg,
  eggnemies: S.Array(Eggnemies),
  isGameOver: S.Boolean,
  score: S.Int,
  ticks: S.Int,
  firstCollisionTick: S.Int, 
})




const initModel = pipe(
  Model.make({
    config: Config.make({
      screenWidth: 600,
      screenHeight: 600,
      fps: 30,
      canvasId: "canvas",
      velocity: 10,
      maxHp: 15,
      eggInvincibilityFrames: 30,
    }),
    egg: Egg.make({
      x: 0,
      y: 0,
      width: 20,
      height: 40,
      vy: 0,
      vx: 0,
      hp: 5,
    }),
    eggnemies: pipe(
      [1,2,3,4,5],
      Array.map((id) =>
        Eggnemies.make({
          x: Math.random() * (600 - 20), 
          y: Math.random() * (600 - 40), 
          width: 20,
          height: 40,
          vx: Math.random() * 2 - 1,
          vy: Math.random() * 2 - 1,
          id,
        }),
      ),
    ),
    isGameOver: false,
    score: 0,
    ticks: 0,
    firstCollisionTick: -30,
  }),
 
  (model) =>
    EggUtils.updateInModel(model, {
      x: model.config.screenWidth / 2 - model.egg.width / 2,
      y: model.config.screenHeight / 2 - model.egg.height / 2,
    }),
)



type Msg = CanvasMsg



const isinCollision = (rect1: Rectangle, rect2: Rectangle) => {
  return (
    rect1.x < rect2.x + rect2.width &&
    rect1.x + rect1.width > rect2.x &&
    rect1.y < rect2.y + rect2.height &&
    rect1.y + rect1.height > rect2.y
  );
}



const updateCollision = (model: Model): Model => {
  const egg = model.egg;
  let Hp = model.egg.hp;
  let firstCollisionTick = model.firstCollisionTick;
  const invincibilityDuration = model.config.eggInvincibilityFrames; 


  const canTakeDamage = model.ticks - firstCollisionTick >= invincibilityDuration;

  if (canTakeDamage) {
    for (const enemy of model.eggnemies) {
      if (isinCollision(egg, enemy)) {
        Hp -= 1; 
        firstCollisionTick = model.ticks; 
        break; 
      }
    }
  }


  return Model.make({
    ...model,
    egg: Egg.make({ ...model.egg, hp: Hp }),
    firstCollisionTick: firstCollisionTick,
  });
}

const updateEgg = (model: Model) =>
  EggUtils.updateInModel(model, {
    y: Math.max(0, Math.min(model.egg.y, model.config.screenHeight - model.egg.height)),
    x: Math.max(0, Math.min(model.egg.x, model.config.screenWidth - model.egg.width)),
  });

const eggnemySpeed = 2;
const updateEggnemies = (model: Model): Model =>
  Model.make({
    ...model,
    eggnemies: model.eggnemies.map(e => {
      if (model.isGameOver) {
        return e;
      }
      const dx = model.egg.x - e.x;
      const dy = model.egg.y - e.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      const normalizedDx = distance === 0 ? 0 : dx / distance;
      const normalizedDy = distance === 0 ? 0 : dy / distance;

      const vx = normalizedDx * eggnemySpeed;
      const vy = normalizedDy * eggnemySpeed;

      return Eggnemies.make({
        ...e,
        x: e.x + vx,
        y: e.y + vy,
      })
    })
  }
  )

const updateTicks = (model: Model) =>
  Model.make({
    ...model,
    ticks: model.ticks + 1,
  });

const updateGameOver = (model: Model) => {
  const egg = model.egg;
  const isGameOver = egg.hp <= 0 || model.eggnemies.length === 0

  if (isGameOver) {
    return Model.make({
      ...model,
      isGameOver: true,
    });
  }

  return model;
}

const updateAttack = (model: Model): Model => {
  if (model.isGameOver) { return model }

  const egg = model.egg;
  const eggnemies = model.eggnemies.filter(eggnemy => (!isinCollision(egg, eggnemy)))
  
  return Model.make({
    ...model,
    eggnemies: eggnemies,
  });

}

export const update = (msg: Msg, model: Model): Model | { model: Model, cmd: Cmd<Msg> } =>
  Match.value(msg).pipe(
    Match.tag("Canvas.MsgKeyDown", ({ key }) => {
      if (model.isGameOver) { return model };

      let x = model.egg.x;
      let y = model.egg.y;
      const velocity = model.config.velocity;

      if (key === "s") {
        y = model.egg.y + velocity;
      } else if (key === "w") {
        y = model.egg.y - velocity;
      } else if (key === "a") {
        x = model.egg.x - velocity;
      } else if (key === "d") {
        x = model.egg.x + velocity;
      } else if (key === "l") {
        return updateAttack(model)
      } else if (key === "r") {
        return initModel
      } else {
        return model
      }
      y = Math.max(0, Math.min(y, model.config.screenHeight - model.egg.height));
      x = Math.max(0, Math.min(x, model.config.screenWidth - model.egg.width));

      return EggUtils.updateInModel(model, { x: x, y: y });
    }),
    Match.tag("Canvas.MsgTick", () =>
      model.isGameOver ? model : (
        pipe(
          model,
          updateEgg, 
          updateEggnemies, 
          updateCollision, 
          updateGameOver,
          updateTicks, 
        )
      ),
    ),
    Match.orElse(() => model),
  );


const view = (model: Model) =>
  pipe(
    model, //
    ({ config, egg }) => [
      Canvas.Clear.make({
        color: "black",
      }),
      Canvas.SolidRectangle.make({
        x: egg.x,
        y: egg.y,
        color: "white",
        height: egg.height,
        width: egg.width
      }),
      Canvas.Text.make({
        x: egg.x + egg.width / 2,
        y: egg.y + egg.height + 15,
        color: "white",
        text: String(model.egg.hp) + "/" + String(model.config.maxHp),
        fontSize: 12,
      }),

      ...model.eggnemies.map(e =>
        Canvas.SolidRectangle.make({
          x: e.x,
          y: e.y,
          color: "gray",
          height: e.height,
          width: e.width,
        }),
      ),

      Canvas.Text.make({
        x: config.screenWidth / 2,
        y: 50,
        text: `${model.score}`,
        color: "black",
        fontSize: 20,
      }),
      viewGameOver(model),
    ],
  )

const viewGameOver = (model: Model) =>
  model.isGameOver ?
    Canvas.Text.make({
      x: model.config.screenWidth / 2,
      y: model.config.screenHeight / 2,
      text: Array.length(model.eggnemies) === 0? "YOU WIN": "GAME OVER",
      color: "white",
      fontSize: 20,
    })
    : Canvas.NullElement.make()

const root = document.getElementById("app")!
const { config } = initModel

startModelCmd(
  root,
  initModel,
  update,
  canvasView(
    config.screenWidth,
    config.screenHeight,
    config.fps,
    config.canvasId,
    view,
  ),
)