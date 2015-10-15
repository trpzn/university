var game = new Phaser.Game(800, 600, Phaser.CANVAS, 'phaser-example', { preload: preload, create: create, update: update, render: render });

//var sprites;
//var rip = 0;

var player;
var cars;
streets = {};
var sidewalks = {};
var activeLane;
var playerInit = {x:400,y:550};
var upKey;
var downKey;
var leftKey;
var rightKey;
var carsGroup;

function preload() {
  game.load.image("road", "../img/_0000_road.png");
  game.load.image("sidewalk", "../img/_0001_restZone.png");
  game.load.image("car","../img/_0001s_0006_policia.png");
  game.load.image("girl","../img/girl.png");
  game.load.image("blood","../img/blood.png");
  game.load.image("resetButton","../img/botonAtropellado.png");

}

spaceRestCount = 600;
playing = true;
function create() {
  game.physics.startSystem(Phaser.Physics.ARCADE);
  carsGroup = game.add.group();
  sidewalks[0] = new Sidewalk();
  streets[0] =  new Road();
  streets[1] =  new Road();
  streets[2] =  new Road();
  streets[3] =  new Road();
  sidewalks[1] = new Sidewalk();



  //console.log(carsGroup);

  upKey = game.input.keyboard.addKey(Phaser.Keyboard.UP);
  downKey = game.input.keyboard.addKey(Phaser.Keyboard.DOWN);
  leftKey = game.input.keyboard.addKey(Phaser.Keyboard.LEFT);
  rightKey = game.input.keyboard.addKey(Phaser.Keyboard.RIGHT);
  //game.time.events.loop(50, createSprite, this);
  player = game.add.sprite(playerInit.x,playerInit.y,"girl");
  //player.scale.set(0.3,0.3);
  game.physics.arcade.enable(player);
  game.world.bringToTop(carsGroup);
}

//to correct bug when player it's dead and car overlap.
function inInitialposition(){
  if(player.position.x == playerInit.x && player.position.y == playerInit.y){
    return true;
  }
  return false;
}

function update() {

  if(playing){
    //check for colition
    if(game.physics.arcade.overlap(carsGroup,player) && !inInitialposition()){
      player.loadTexture("blood");
      showResetButton();
      console.log("you died");
      playing = false;
      return;
    }

    //movement
    if (upKey.isDown)
    {
        player.y--;
    }
    else if (downKey.isDown)
    {
        player.y++;
    }

    if (leftKey.isDown)
    {
        player.x--;
    }
    else if (rightKey.isDown)
    {
        player.x++;
    }
  }
}

function render() {

}

function createMap(initSidewalk, player){
  if(initsidewalk == 'undefined'){

  }
}

function Sidewalk(){
  //console.log(1);
  this.spriteGreen = game.add.sprite(0,spaceRestCount-55,"sidewalk");
  spaceRestCount -= 55;
}

function Road(){
  this.spriteRoad = game.add.sprite(0,spaceRestCount-110,"road");
  spaceRestCount -= 110;
  this.tracks = {};
  this.tracks[0] = new track(this.spriteRoad.position.y + 10,300);
  this.tracks[1] = new track(this.spriteRoad.position.y + 60,400);
}

var minDistance = 200;


function track(initPosition,traffic,maxVelocity){
  this.initPosition = initPosition;
  this.traffic = traffic;
  this.maxVelocity = maxVelocity;

  if(this.traffic<=minDistance) this.traffic = minDistance; //asegurar que no se rompa la distancia minima
  this.traffic = game.rnd.between(minDistance,traffic); //randomizar la distancia
  //console.log(traffic);
  this.xStartPositions = [800,0]; //posiciones iniciales de los puntos de partida
  this.ystartPosition = initPosition;
  this.direction = game.rnd.between(0,1); // 0 left - 1 Right
  this.carsInTrack = []; //autos instanciados en este track
  this.trackInstance = this;
  this.launchNewCar(this.xStartPositions[this.direction],this.ystartPosition,this.direction);
}

track.prototype = {
   launchNewCar: function(x,y,direction){
    //no existen autos instanciados
    if(this.carsInTrack.length == 0){
      this.carsInTrack[0] = new Car(x,y,direction,this.trackInstance,100,this.traffic,this.launchNewCar);
    }else{
      //buscar por autos instanciados deshabilitados
        for(idCars in this.carsInTrack){
          car = this.carsInTrack[idCars];
          //console.log(car.spriteCar);

          if(!car.enabled){
            //auto que no se esta ocupando habilitar
            car.enableCar(x);
            return;
          }
        }
        //no se encontro ningun auto deshabilitado crear una nueva instanciados
        this.carsInTrack[this.carsInTrack.length] = new Car(x,y,direction,this.trackInstance,100,this.traffic,this.launchNewCar);
    }
  }
}
var carcount =0;
function Car(x,y,direction,trackInstance,velocity,launchDistance,launchNewCar){
  //console.log("Car created");
  //construct car
  carcount++;
  this.x = x;
  this.y = y;
  this.direction = direction;
  this.trackInstance = trackInstance;
  this.velocity = velocity;
  this.launchDistance = launchDistance;
  this.spriteCar = game.add.sprite(x,y,"car");
  carsGroup.add(this.spriteCar);
  //this.spriteCar.bringToTop();


  game.physics.arcade.enable(this.spriteCar);
  if(direction==0) direction = -1;
  this.spriteCar.body.velocity.x = velocity * (direction);

  this.enabled;
  this.distanceFromInit = 0;

  var updateTimer; //event that update car if enabled
  this.launchedCar = false;

  this.spriteCar.update = this.carUpdate;
  this.update; //timer event
  this.enableCar();
}

Car.prototype = {
  carUpdate: function(){

    if(this.enabled){


      if(!this.spriteCar.inWorld){
        //console.log("car not visible");
        //el auto deja de ser visible
        this.disableCar();
        //console.log("auto desactivado");
      }else{
        //el auto aun es visible
        this.calculateDistance();
      //  console.log(distanceFromInit+ "-" +launchDistance);
        if(!this.launchedCar && this.distanceFromInit >= this.launchDistance){
          //el auto alcanzo la distancia para que aparezca el siguiente auto
          this.launchedCar = true;
          this.trackInstance.launchNewCar.call(this.trackInstance,this.x,this.y,this.direction);
        }
      }
    }
  },

  enableCar: function(){
    //console.log("auto habilidado");
    this.enabled = true;
    this.spriteCar.position.x = this.x;
    this.update = game.time.events.loop(50,this.carUpdate,this);
  },

  disableCar: function(){
    //console.log("auto deshabilidado");
    this.enabled = false;
    this.launchedCar = false;
    game.time.events.remove(this.update);
    this.update = 'undefined';
  },

  calculateDistance: function(){
    if(this.direction>0){
      this.distanceFromInit = this.spriteCar.position.x;
    }else{
      this.distanceFromInit = 800-this.spriteCar.position.x;
    }
  }


}



var resetButtonSprite;

function showResetButton(){
  resetButtonSprite = game.add.button(200, 0, 'resetButton', pressedResetButton, this);
}

function pressedResetButton(){
  console.log("hola");
  resetButtonSprite.destroy();
  playing = true;
  player.loadTexture("girl");
  player.position.x = playerInit.x;
  player.position.y = playerInit.y;
}
