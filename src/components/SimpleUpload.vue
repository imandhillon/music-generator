<template>
    <form @submit.prevent="sendFile" enctype="multipart/form-data">

    <nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container-fluid">
        <div class="navbar-header">
        <a class="navbar-brand" href="#">AudioGen</a>
        </div>
        <ul class="nav navbar-nav">
        <li class="active"><a href="imandhillon.com">imandhillon.com</a></li>
        </ul>
    </div>
    </nav>



    <div class="mainimgbox">
    <img class="mainimg" src="./musicwavescrop2.jpg" width="2000" height="30">
    </div>

    <div id='instructions'>
        <br>Click or drag a .wav file onto the dropzone that sounds similar to the sound you want.<br> Then click the Generate Audio button and enjoy!
    </div>

    <div v-if="msg"
        :class="`msg ${error ? 'is-danger' : 'is-success'}`" >
        <div class="msg-body">{{msg}}
        </div>
    </div>



        <div class="gen">
            <button class="button is-info" id="genBtn" disabled="true">Send and Generate Audio</button>

        </div>

        <div id="dropzone">
            <vue-dropzone id="drop1" :options="dropOptions" ref="myVueDropzone"
            @vdropzone-file-added="vfileAdd"
            
            ></vue-dropzone>
            
        </div>



        <div class="dz-av">

        <div id="audiovis">
            <div v-if="loading"
                class="loadspin">
                <img class="spinner" src="./Wedges-3s-207px-trans.gif" width="80" height="80">
            </div>
            <canvas id='canvas' width="800" height="150"></canvas>
            <br>
            <br>
            <audio crossOrigin="anonymous"
                :src = "initAudio"
                id = "audio" controls>
                audio element not supported
            </audio>
        </div>

        </div>

        <!-- <av-bars
            audio-src="http://127.0.0.1:5000/api/getfile/new.wav">
        </av-bars> -->
        <!-- <av-bars
        :canv-top="true"
        :canv-width="600"
        :canv-height="120"
      caps-color="#FFF"
      :bar-color="['#f00', '#ff0', '#0f0']"
      canv-fill-color="#000"
      :caps-height="2"
      audio-src="http://127.0.0.1:5000/api/getfile/new.wav"
    ></av-bars> -->
            

        <span v-if="file" class="file-name">
            {{file.name}} 
        </span>

        
    </form>


</template>

<script>
/* eslint-disable */
import axios from 'axios';
import vueDropzone from "vue2-dropzone";
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import AudioVisual from 'vue-audio-visual';

export default {
    name: "SimpleUpload",
    data() {
        return{
            file: "",
            msg: "",
            error: false,
            uploading: false,
            canGen: false,
            count: 0,
            loading: false,
            isDisabled: true,
            filepath: "",
            firstGen: "1",

            dzDisabled: false,
            dropOptions: {
                url: "http://127.0.0.1:5000/api/sendaudio",
                acceptedFiles: 'audio/wav',
                maxFilesize: 200,
                autoProcessQueue: false,
                maxFiles: 1,
    
            }
        }
    },
    components: {
        vueDropzone,
    },
    methods: {
        vfileAdd(file) {
            var genBtn = document.getElementById("genBtn"); 
            genBtn.disabled = false;
        },
        
        async sendFile() {
            const formData = new FormData();
            this.file = this.$refs.myVueDropzone.getAcceptedFiles()[0]
            formData.append('file', this.file)
            try {
                // if we click send without having selected a file, 
                console.log(this.$refs.myVueDropzone.getAcceptedFiles())
                this.loading = true;
                

                await axios.post("http://127.0.0.1:5000/api/sendaudio", formData)
                .then(response => {
                    this.filepath = response.data.uploadPath
                    console.log(this.filepath, 'uploaded file')
                    this.$refs.myVueDropzone.removeAllFiles()
                    this.$refs.myVueDropzone.disable()
                    this.canGen = true

                    this.msg = "File uploaded"
                    this.file = ""
                    this.error = false
                    console.log('in send')
                    this.genAudio()
                })
                .catch(error => {
                    this.msg = "File failed to upload"
                    console.log(error)
                })
                
            }
            catch(err) {
                this.msg = err.response.data.error
                this.error = true
            }
        },
        genAudio() {
            if (this.canGen === true){
                var genBtn = document.getElementById("genBtn"); 
                genBtn.disabled = true;
                console.log(this.filepath, 'filepath')
                const formData = new FormData();
                formData.append('filePath', this.filepath)
                formData.append('firstGen', this.firstGen)
                axios.post('http://127.0.0.1:5000/api/generate', formData)
                .then(response => {
                    this.initAudio();
                })
            }
            if (this.canGen === false){
                console.log(this.canGen)
            }
        },
        initAudio(removeAudioFlag) {
            this.canGen = false;

            var audioRemove = document.getElementById("audio");
            audioRemove.remove();

            document.getElementById('audiovis').insertAdjacentHTML('beforeend', "<audio id='audio', src='http://127.0.0.1:5000/api/getfile/new.wav' crossOrigin='anonymous' controls></audio>");
            var audio = document.getElementById("audio");
            var ctx = new AudioContext();

            var analyser = ctx.createAnalyser();
            var audioSrc = ctx.createMediaElementSource(audio);
            
            // Connect the MediaElementSource with the analyser 
            audioSrc.connect(analyser);
            analyser.connect(ctx.destination);
    
            this.showVisualizer(audioSrc, analyser, ctx, audio);
        },
        showVisualizer(audioSrc, analyser, ctx, audio) {
            //this.$refs.myVueDropzone.enable();
            this.canGen = true;
            //var genBtn = document.getElementById("genBtn"); 
            //genBtn.disabled = false;
            // Credit to Cornelius Gee for the Visualizer code. https://codepen.io/cgyc8866/pen/wGRqLw

            // we could configure the analyser: e.g. analyser.fftSize (for further infos read the spec)
            // analyser.fftSize = 64;
            // frequencyBinCount tells you how many values you'll receive from the analyser
            var frequencyData = new Uint8Array(analyser.frequencyBinCount);

            // we're ready to receive some data!
            var canvas = document.getElementById('canvas'),
                cwidth = canvas.width,
                cheight = canvas.height - 2,
                meterWidth = 10, //width of the meters in the spectrum
                gap = 2, //gap between meters
                capHeight = 2,
                capStyle = '#39FF14',
                meterNum = 800 / (10 + 2), //count of the meters
                capYPositionArray = []; ////store the vertical position of hte caps for the preivous frame
            ctx = canvas.getContext('2d'),
            console.log(ctx);
            // gradient = ctx.createLinearGradient(0, 0, 0, 300);
            // gradient.addColorStop(1, '#0f0');
            // gradient.addColorStop(0.5, '#ff0');
            // gradient.addColorStop(0, '#f00');
            // loop
            function renderFrame() {
                var array = new Uint8Array(analyser.frequencyBinCount);
                analyser.getByteFrequencyData(array);
                var step = Math.round(array.length / meterNum); //sample limited data from the total array
                ctx.clearRect(0, 0, cwidth, cheight);
                for (var i = 0; i < meterNum; i++) {
                    var value = array[i * step];
                    if (capYPositionArray.length < Math.round(meterNum)) {
                        capYPositionArray.push(value);
                    };
                    ctx.fillStyle = capStyle;
                    //draw the cap, with transition effect
                    if (value < capYPositionArray[i]) {
                        ctx.fillRect(i * 12, cheight - (--capYPositionArray[i]), meterWidth, capHeight);
                    } else {
                        ctx.fillRect(i * 12, cheight - value, meterWidth, capHeight);
                        capYPositionArray[i] = value;
                    };
                    // ctx.fillStyle = gradient; //set the fillStyle to gradient for a better look
                    ctx.fillRect(i * 12 /*meterWidth+gap*/ , cheight - value + capHeight, meterWidth, cheight); //the meter
                }
                requestAnimationFrame(renderFrame);
            }
            renderFrame();

            this.loading = false;
            audio.play();
            this.firstGen = "2"
        },

    },
    computed: {
    

         disableGenerate () {
             if (this.canGen == false) {
                var genBtn = document.getElementById("genBtn"); 
                genBtn.disabled = true;
             }
        },
    },
    
}
</script>


<style scoped>
    form {
        background-color: rgb(230, 230, 230);
        text-align: center;
    }
    .dz-av{
        display: flex;
        justify-content: center;
        width: 100%;
        height: 250px;
    }
    .dropzone {
        min-height: 150px;
        width: 80%;
        padding: 10px 10px;
        position: relative;
        
        margin: auto;
        cursor: pointer;
        outline: 2px dashed rgb(109, 109, 109);
        outline-offset: -10px;
        background: rgb(176, 255, 255);
        color: dimgray;
    }
    .loadspin {
        display: flex;
        position: absolute;
        margin-left: auto;
        margin-right: auto;
        left: 0;
        right: 0; 
        justify-content: center;
    }
    .audiovis {
        z-index: 1;
        position: relative;
        justify-content: flex-start;
    }
    .audio {
        justify-content: center;
    }
    .canvas {
        position: absolute;
        justify-content: center;
        z-index: 1;
    }

    .input-file {
        opacity: 0;
        width: 100px;
        height: 200px;
        position: absolute;
        cursor: pointer;
    }

    .dropzone:hover {
        color: rgb(5, 60, 78);
        background: rgb(234, 136, 243);
    }
    .gen{
        margin: auto;
        text-align: center;
        padding: 15px;
        font-family: Helvetica ,Arial, serif
    }
    a{
        color:yellow;
    }
    .bar-wrapper {
        height: 300px;
        position: relative;
    }
    .bar {
        position: relative;
        bottom: 0;
        width: 5px;
        display: inline-block;
        border: 1px solid red;
        height: 5px;
        border-bottom: 3px solid rgb(255, 17, 17);
    }
    .instructions {
        display: inline-block;
    }
    .resetBtn {
        font-family: Times, Arial, Helvetica, sans-serif;
        color:rgb(255, 255, 255);
        margin: auto;
        text-align: center;
        padding: 15px;
        padding-bottom: 25px;
    }
    .reset {
        padding-bottom: 40px;
    }
    .v-btn {
        text-transform:none !important;
        font-size: 18px;
        font-family: Arial, Helvetica, sans-serif;
        font-weight:550;

    }

</style>