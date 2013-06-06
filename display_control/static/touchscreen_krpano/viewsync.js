console.log( 'initializing viewsync' );

var yawoffset = (fields.yawoffset) ? fields.yawoffset : 0;
var pitchoffset = (fields.pitchoffset) ? fields.pitchoffset : 0;
var rolloffset = (fields.rolloffset) ? fields.rolloffset : 0;

var urlImage = (fields.rolloffset) ? fields.rolloffset : 'defaultpano.jpg';

var viewsync = io.connect('/viewsync');

var curxml = "";

viewsync.on('connect', function() {
  console.log('viewsync connected');
    viewsync.on('sync video', function(data) {
      var pano = krPano();
      if ('set' in pano) {
	console.log('seeking:' + data.time );
        pano.call(
	  'plugin[video].seek( ' + data.time + ' );'
	);
      }
    });
    viewsync.on('sync pano', function (data) {
      console.log('pano: ' + data.xmlname);
      var pano = krPano();
      pano.call("loadpano(" + data.xmlname + ", null, MERGE, BLEND(1));");
    });
  if(fields.master == "true") {
    // events for master
    console.log('master of the universe');
  } else {
    // events for slaves
    viewsync.on('sync pov', function(data) {
      var pano = krPano();
      if ('set' in pano) {
        // do offset math here?
        pano.call(
          'set( yawoffset, ' + yawoffset + ' );'
        + 'set( pitchoffset, ' + pitchoffset + ' );'
        + 'set( rolloffset, ' + rolloffset + ' );'
        + 'set( master_h, ' + data.hlookat + ' );'
        + 'set( master_v, ' + data.vlookat + ' );'
        + 'set( master_r, ' + data.camroll + ' );'
        + 'set( master_f, ' + data.fov + ' );'
        + 'viewShift();'
	//+ 'plugin[video].seek( ' + data.time + ' );'
        //+ 'set( view.fov, ' + data.fov + ' );'
        );
  	console.log(data.time);
      } else {
        console.log( 'ignoring fov, pano not initialized' );
      }
    });
  }
});

viewsync.on('connect_failed', function() {
  console.log('viewsync connected');
});
viewsync.on('disconnect', function() {
  console.log('viewsync disconnected');
});

function viewsync_send_pov() {
  var pano = krPano();
  var data = {
    hlookat: pano.get( 'view.hlookat' ),
    vlookat: pano.get( 'view.vlookat' ),
    camroll: pano.get( 'view.camroll' ),
    fov: pano.get( 'view.fov' ),
    time: pano.get( 'plugin[video].time' )
  };
  /*console.log( pano.getattributes() );*/
  //pano.call('trace( 1, ' + data + ');');
  viewsync.emit( 'pov', data );
  /*console.log(data);*/
}

function viewsync_send_pano() {
  if (curxml != "") {
    var pano = krPano();
    var data = { xmlname: curxml };
    viewsync.emit( 'pano', data );
  }
}

// external, temporary, hack
function loadpano( xmlname ) {
  viewsync.emit('pano', { xmlname: xmlname });
}
function seek( time ) {
  viewsync.emit('video', { time: time });
  console.log('seek:' + time);
}

if (fields.master == "true") {
  var multiaxis = io.connect('/multiaxis');
  multiaxis.on('connect',function() {
          console.log('MultiAxis connected');
  });

  var NAV_SENSITIVITY = 0.005;
  var NAV_GUTTER_VALUE = 12;

  multiaxis.on('axis',function(data) {
    console.log('multiaxis abs: ' + data.abs);
    var v = 0;
    var h = 0;
    var f = 0;
    var value;
    var dirty = false;
    for( var axis in data.abs ) {
      switch(axis) {
        case '3':
          value = data.abs[axis];
          if( Math.abs( value ) > NAV_GUTTER_VALUE ) {
            v = value * NAV_SENSITIVITY;
            dirty = true;
          }
          break;
        case '5':
          value = data.abs[axis];
          if( Math.abs( value ) > NAV_GUTTER_VALUE ) {
            h = value * NAV_SENSITIVITY;
            dirty = true;
          }
          break;
        case '1':
          value = data.abs[axis];
          if( Math.abs( value ) > NAV_GUTTER_VALUE ) {
            f = value * NAV_SENSITIVITY;
            dirty = true;
          }
          break;
      }
    }
    if (dirty) {
      console.log( 'updating view from multiaxis state' );
      var pano = krPano();
      pano.call(
        'add( view.vlookat, get( view.vlookat ), ' + -v + ' );'
      + 'add( view.hlookat, get( view.hlookat ), ' + h + ' );'
      + 'add( view.fov, get( view.fov ), ' + f + ' );'
      );
    }
  });

  multiaxis.on('disconnect',function() {
          console.log('MultiAxis disconnected');
  });
}
