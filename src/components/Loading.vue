<template>
    <div class="loading">
         <div class="spinner spinner-1"></div>
    </div>
 </template>

 <script>

 export default {
   name: 'Loading',

   data () {
     return {}
    }
 }
 </script>

 <!-- Add "scoped" attribute to limit CSS to this component only -->
 <style scoped>
.spinner {
  position: relative;
  width: 125px;
  height: 125px;
}

.spinner:before, .spinner:after {
  content: "";
  display: block;
  position: absolute;
  border-width: 4px;
  border-style: solid;
  border-radius: 50%;
}

@-webkit-keyframes rotate-animation {
  0% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
  }
}
@keyframes rotate-animation {
  0% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
  }
}
@-webkit-keyframes anti-rotate-animation {
  0% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(-360deg);
            transform: rotate(-360deg);
  }
}
@keyframes anti-rotate-animation {
  0% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(-360deg);
            transform: rotate(-360deg);
  }
}
.spinner.spinner-1:before {
  width: 117px;
  height: 117px;
  border-bottom-color: #212121;
  border-right-color: #212121;
  border-top-color: rgba(33, 33, 33, 0);
  border-left-color: rgba(33, 33, 33, 0);
  top: 0px;
  left: 0px;
  -webkit-animation: rotate-animation 1s linear 0s infinite;
          animation: rotate-animation 1s linear 0s infinite;
}
.spinner.spinner-1:after {
  width: 81.9px;
  height: 81.9px;
  border-bottom-color: #212121;
  border-right-color: #212121;
  border-top-color: rgba(33, 33, 33, 0);
  border-left-color: rgba(33, 33, 33, 0);
  top: 17.55px;
  left: 17.55px;
  -webkit-animation: anti-rotate-animation 0.85s linear 0s infinite;
          animation: anti-rotate-animation 0.85s linear 0s infinite;
}

 </style>
