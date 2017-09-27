//= require_tree .
//= require websocket_rails/main

console.log('connecting');
var dispatcher = new WebSocketRails('localhost:5000/websocket');

dispatcher.on_open = (data) => {
  console.log('Connection has been established: ', data);
  // You can trigger new server events inside this callback if you wish.
};

dispatcher.on_error = (err) => console.log(err);

dispatcher.bind('connection_closed', (data) => {
  console.log('connection is closed');
});
dispatcher.bind('connection_opened', (data) => {
  console.log('connection is opened');
});

window.dispatcher = dispatcher; // so you can test in the console
