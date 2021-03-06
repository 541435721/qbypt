/**
 * Created by bxsh on 2016/8/23.
 */

if (!Detector.webgl) Detector.addGetWebGLMessage();

function doNothing() {
    window.event.returnValue = false;
    return false;
}
color_board = new Array();
var container, stats;
var camera, cameraTarget, scene, renderer;

var camera_p_x = 100;
var camera_p_y = 0;
var camera_p_z = 0;
var count = 0;
var sta = 0;

var mesh_r_x = -Math.PI / 2;
var mesh_r_y = 0;
var mesh_r_z = 0;

var start_x = 0;
var start_y = 0;


var color = new Array(
    '#FFE4C4',
    '#ff5533',
    '#D2691E',
    '#483D8B',
    '#D19275',
    '#FF69B4',
    '#A52A2A',
    '#008000',
    '#FF8C00',
    '#0000FF',
    '#00ffff',
    '#00008b',
    '#e9967a',
    '#1e90ff',
    '#ff00ff',
    '#ffa500',
    '#4682b4',
    '#9acd32'
);

// new added
var labels = new Array();
var COLORS = new Array();
for (var iii = 0; iii <= 16; iii++) {
    COLORS.push('#ffffff');
    labels.push(0);
}

//var d = document.getElementById('p');
//d.setAttribute('name', 'd');

var X = 0;
var Y = 0;

var controls;
container = document.createElement('div');
container.setAttribute("id", "div");

//document.body.appendChild(container);
var canvas_div = document.getElementById('canvas_div');
canvas_div.appendChild(container);


camera = new THREE.PerspectiveCamera(50, window.innerWidth * 10 / 12 / window.innerHeight, 0.1, 10000);
camera.position.set(camera_p_x, camera_p_y, camera_p_z);

cameraTarget = new THREE.Vector3(0, 0, 0);

scene = new THREE.Scene();

var intensity = 0.5;

var light = new THREE.AmbientLight(0x404040); // soft white light


var light1 = new THREE.DirectionalLight(0xffffff, intensity);
var light2 = new THREE.DirectionalLight(0xffffff, intensity);
var light3 = new THREE.DirectionalLight(0xffffff, intensity);
var light4 = new THREE.DirectionalLight(0xffffff, intensity);
var light5 = new THREE.DirectionalLight(0xffffff, intensity);
var light6 = new THREE.DirectionalLight(0xffffff, intensity);

var or = 1;
light1.position.set(0, 0, or);
light2.position.set(0, or, 0);
//light3.position.set(or, 0, 0);
light4.position.set(0, 0, -1 * or);
light5.position.set(0, -1 * or, 0);
light6.position.set(-1 * or, 0, 0);

scene.add(light1);
scene.add(light2);
scene.add(light3);
scene.add(light4);
scene.add(light5);
scene.add(light6);

scene.add(light);


renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setClearColor(0x000000);
renderer.setSize(window.innerWidth * (10 / 12) * 0.8, (window.innerHeight - 30) * 0.3);
// renderer.setSize(canvas_div.clientWidth, canvas_div.clientHeight);
renderer.domElement.setAttribute('id', 'cvs');
//renderer.domElement.addEventListener('mousewheel', scaleCanvas, false);

container.appendChild(renderer.domElement);
controls = new THREE.TrackballControls(camera, renderer.domElement);
controls.addEventListener('change', render);
//controls.autoRotate = true;
controls.rotateSpeed = 5.0;
controls.zoomSpeed = 1.0;
controls.panSpeed = 0.8;

controls.noZoom = false;
controls.noPan = false;

controls.staticMoving = true;
controls.dynamicDampingFactor = 0.3;

controls.keys = [65, 83, 68];


stats = new Stats();
stats.domElement.style.position = 'absolute';
stats.domElement.style.top = '0px';
//container.appendChild(stats.domElement);
camera.position.set(camera_p_x, camera_p_y, camera_p_z);

camera.position.set(camera_p_x, camera_p_y, camera_p_z);
camera.lookAt(cameraTarget);
//修改元素宽度的方法，window.innerHeight代表窗口当前的宽度
renderer.setSize(canvas_div.clientWidth, window.innerHeight);
//根据窗口宽度的变化来改变元素宽度
window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
    renderer.setSize(canvas_div.clientWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    controls.handleResize();
}

function show_single_stl(path, id, opa) {
    var loader = new THREE.STLLoader();         // new 一个load加载对象
    var mesh;                                   // 申明一个mesh变量
    var index = layer.load(1, {
        shade: [0.4, '#fff'] //0.1透明度的白色背景
    });
    count++;
    loader.load(path, function (geo) {
        if (scene.children.length - 7 == 0) {
            offset = geo.center();
        }// loader的初始化
        else {
            try {
                geo.translate(offset.x, offset.y, offset.z);
            } catch (e) {
                alert(e);
            }

            //alert(id + " " + offset.x + " " + offset.y + " " + offset.z);
        }
        // 将其放入最中间位置
        var num = path.lastIndexOf(".stl");     // 读取是第几个stl
        //var p = document.getElementById('dis' + path.substring(path.lastIndexOf("/") + 1, num));
        //p.innerHTML = "X:" + calculateSize(geo)[0] + " Y:" + calculateSize(geo)[1] + " Z:" + calculateSize(geo)[2];

        var material = new THREE.MeshPhongMaterial({        //加载材料
            // color: color[c],
            specular: 0x001111,
            shininess: 10,
            wireframe: false,
            //side: THREE.doubleSided,
            transparent: true,
            opacity: opa,
            side: THREE.DoubleSide,
        });
        // if (labels[id - 1] == 1) {
        //     material.color = new THREE.Color(COLORS[id - 1]);
        // } else {
        //     // material.color = new THREE.Color(color[c]);
        // }
        material.color = new THREE.Color(color[id % color.length]);     //加载不通的颜色
        mesh = new THREE.Mesh(geo, material);               //合并成一个mesh


        mesh.position.set(0, 0, 0);
        mesh.rotation.set(mesh_r_x, mesh_r_y, mesh_r_z);  //加载位置设置
        mesh.scale.set(0.2, 0.2, 0.2);                  // 加载的大小设置

        mesh.castShadow = true;             //阴影
        mesh.receiveShadow = true;
        mesh.name = 'actor' + id;           //定义名字
        scene.add(mesh);                       //场景加入mesh
        count--;
        if (count <= 0) {
            layer.closeAll('loading'); //关闭加载层
        }
    });
}


function show_all_stl(path, id, opa) {
    var loader = new THREE.STLLoader();
    var mesh;
    offset = 0;
    loader.load(path, function (geo) {
        if (offset == 0) {
            offset = geo.center();
        } else {
            try {
                geo.translate(offset.x, offset.y, offset.z);
            } catch (e) {
                alert(e);
            }

            //alert(id + " " + offset.x + " " + offset.y + " " + offset.z);
        }


        var material = new THREE.MeshPhongMaterial({
            color: color_board[parseInt(id)],
            specular: 0x001111,
            shininess: 80,
            wireframe: false,
            //side: THREE.doubleSided,
            transparent: true,
            opacity: opa,
        });

        material.color = new THREE.Color(color_board[parseInt(id)]);
        mesh = new THREE.Mesh(geo, material);

        //alert(mesh.position.x + " " + mesh.position.y + " " + mesh.position.z);
        //mesh.position.set(0, 0, 0);
        mesh.rotation.set(mesh_r_x, mesh_r_y, mesh_r_z);
        mesh.scale.set(0.2, 0.2, 0.2);

        mesh.castShadow = true;
        mesh.receiveShadow = true;
        mesh.name = 'actor' + (parseInt(id) + 1);

        scene.add(mesh);

    });
}


function render() {

    var timer = Date.now() * 0.005;
    controls.autoRotate = false;
    // camera.position.x = Math.cos(timer) * 0.01;
    // camera.position.y = Math.sin( timer ) * 1;
    renderer.render(scene, camera);
}

function auto_rotate(parts) {
    for (var part_index = 0; part_index < parts; part_index++) {
        selectedObject = scene.getObjectByName('actor' + part_index);
        if (selectedObject) {
            selectedObject.rotation.z += 0.04;
        }
    }
    requestAnimationFrame(auto_rotate);
    renderer.render(scene, camera);
}
function cancle_rotate(parts) {
    for (var part_index = 0; part_index < parts; part_index++) {
        selectedObject = scene.getObjectByName('actor' + part_index);
        if (selectedObject) {
            selectedObject.rotation.z -= 0.04;
        }
    }
    requestAnimationFrame(cancle_rotate);
    renderer.render(scene, camera);
}

function scaleCanvas(event) {
    var e = window.event || event; // old IE support
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
    //var p = document.getElementById('te');

    if (delta == 1) {//放大
        camera_p_x -= 2;
        //camera_p_y -= 1;
        //camera_p_z -= 1;
    }
    if (delta == -1) {//缩小
        camera_p_x += 2;
        //camera_p_y += 1;
        //camera_p_z += 1;
    }

    //p.innerHTML = delta + "->" + e.wheelDelta + '->' + e.detail + ' ' + camera_p_x;
}

function animate() {
    requestAnimationFrame(animate);
    render();
    controls.update();
    stats.update();
}

function calculateVol(geo) {
    var x1, x2, x3, y1, y2, y3, z1, z2, z3, i;
    var len = geo.faces.length;
    var totalVolume = 0;
    var totalArea = 0;
    var a, b, c, s;

    for (i = 0; i < len; i++) {
        x1 = geo.vertices[geo.faces[i].a].x;
        y1 = geo.vertices[geo.faces[i].a].y;
        z1 = geo.vertices[geo.faces[i].a].z;
        x2 = geo.vertices[geo.faces[i].b].x;
        y2 = geo.vertices[geo.faces[i].b].y;
        z2 = geo.vertices[geo.faces[i].b].z;
        x3 = geo.vertices[geo.faces[i].c].x;
        y3 = geo.vertices[geo.faces[i].c].y;
        z3 = geo.vertices[geo.faces[i].c].z;

        totalVolume +=
            (-x3 * y2 * z1 +
            x2 * y3 * z1 +
            x3 * y1 * z2 -
            x1 * y3 * z2 -
            x2 * y1 * z3 +
            x1 * y2 * z3);

        a = geo.vertices[geo.faces[i].a].distanceTo(geo.vertices[geo.faces[i].b]);
        b = geo.vertices[geo.faces[i].b].distanceTo(geo.vertices[geo.faces[i].c]);
        c = geo.vertices[geo.faces[i].c].distanceTo(geo.vertices[geo.faces[i].a]);
        s = (a + b + c) / 2;
        totalArea += Math.sqrt(s * (s - a) * (s - b) * (s - c));
    }

    return [Math.abs(totalVolume / 6).toFixed(2), totalArea.toFixed(2)];
}


function calculateSize(geo) {

    var x_l = geo.boundingBox.max.x - geo.boundingBox.min.x;
    var y_l = geo.boundingBox.max.y - geo.boundingBox.min.y;
    var z_l = geo.boundingBox.max.z - geo.boundingBox.min.z;
    return new Array(x_l.toFixed(2), y_l.toFixed(2), z_l.toFixed(2));
}

document.getElementById('cvs').onmousedown = function (event) {

}
document.onkeydown = function (event) {
    var a = 3;
    rato1 = 2 * Math.PI / 360 * a;
    num = scene.children.length - 7;
    if (event.keyCode == 39) { //右键39
        for (var part_index = 0; part_index <= num; part_index++) {
            selectedObject = scene.getObjectByName('actor' + part_index);
            if (selectedObject) {
                selectedObject.rotation.z += rato1;
            }
        }
    } else if (event.keyCode == 37) { //左键37
        for (var part_index = 0; part_index <= num; part_index++) {
            selectedObject = scene.getObjectByName('actor' + part_index);
            if (selectedObject) {
                selectedObject.rotation.z -= rato1;
            }
        }
    } else if (event.keyCode == 38) {// 上键38
        selectedObject = scene.getObjectByName('actor' + part_index);
        for (var part_index = 0; part_index <= num; part_index++) {
            selectedObject = scene.getObjectByName('actor' + part_index);
            if (selectedObject) {
                selectedObject.rotation.y -= rato1;
            }
        }
    } else if (event.keyCode == 40) {//下键40
        selectedObject = scene.getObjectByName('actor' + part_index);
        for (var part_index = 0; part_index <= num; part_index++) {
            selectedObject = scene.getObjectByName('actor' + part_index);
            if (selectedObject) {
                selectedObject.rotation.y -= rato1;
            }
        }
    }
}
document.onkeyup = function (event) {
    if (event.keyCode == 39) { //右键39

    } else if (event.keyCode == 37) { //左键37

    } else if (event.keyCode == 38) {// 上键38

    } else if (event.keyCode == 40) {//下键40

    }
}