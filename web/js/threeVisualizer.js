import * as THREE from 'three';
import { api } from '../../../scripts/api.js'

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';

const visualizer = document.getElementById("visualizer");
const container = document.getElementById( 'container' );
const progressDialog = document.getElementById("progress-dialog");
const progressIndicator = document.getElementById("progress-indicator");

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize( window.innerWidth, window.innerHeight );
container.appendChild( renderer.domElement );

const pmremGenerator = new THREE.PMREMGenerator( renderer );

// scene
const scene = new THREE.Scene();
scene.background = new THREE.Color( 0x000000 );
scene.environment = pmremGenerator.fromScene( new RoomEnvironment( renderer ), 0.04 ).texture;

const ambientLight = new THREE.AmbientLight( 0xffffff );

const camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 1, 100 );
camera.position.set( 5, 2, 8 );
const pointLight = new THREE.PointLight( 0xffffff, 15 );
camera.add( pointLight );

const controls = new OrbitControls( camera, renderer.domElement );
controls.target.set( 0, 0.5, 0 );
controls.update();
controls.enablePan = true;
controls.enableDamping = true;

// Handle window reseize event
window.onresize = function () {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

};


var lastFilepath = "";
var needUpdate = false;

function frameUpdate() {
    
    var filepath = visualizer.getAttribute("filepath");
    if (filepath == lastFilepath){
        if (needUpdate){
            controls.update();
            renderer.render( scene, camera );
        }
        requestAnimationFrame( frameUpdate );
    } else {
        needUpdate = false;
        scene.clear();
        progressDialog.open = true;
        lastFilepath = filepath;
        main(JSON.parse(lastFilepath));
    }
}

const onProgress = function ( xhr ) {
    if ( xhr.lengthComputable ) {
        progressIndicator.value = xhr.loaded / xhr.total * 100;
    }
};
const onError = function ( e ) {
    console.error( e );
};

async function main(params) {
    if(params?.filename){
        const url = api.apiURL('/view?' + new URLSearchParams(params)).replace(/extensions.*\//,"");
        const fileExt = params.filename.slice(params.filename.lastIndexOf(".")+1)

        if (fileExt == "obj"){
            const loader = new OBJLoader();

            loader.load( url, function ( obj ) {
                obj.scale.setScalar( 5 );
                console.log(obj)
                scene.add( obj );
                obj.traverse(node => {
                    if (node.material && node.material.map == null) {
                        node.material.vertexColors = true;
                    }
                  });

            }, onProgress, onError );
        }

        needUpdate = true;
    }

    scene.add( ambientLight );
    scene.add( camera );

    progressDialog.close();

    frameUpdate();
}

main();