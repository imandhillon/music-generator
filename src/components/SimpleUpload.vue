<template>
    <form @submit.prevent="sendFile" enctype="multipart/form-data">

    <!-- <header>
        <h1>Music Generator</h1>
        <h2>Input a .wav file that is similar to what you want to hear<br><br></h2>
    </header> -->

    <nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container-fluid">
        <div class="navbar-header">
        <a class="navbar-brand" href="#">AudioGen</a>
        </div>
        <ul class="nav navbar-nav">
        <li class="active"><a href="imandhillon.com">imandhillon.com</a></li>
        <!-- <li><a href="#">Page 1</a></li>
        <li><a href="#">Page 2</a></li>
        <li><a href="#">Page 3</a></li> -->
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

        <!-- <div class="field">

            <div class="file is boxed is-primary" disabled>
                <label class="file-label">

                    <input type="file"
                        ref="file"
                        @change="selectFile"
                        class="file-input"
                    />
                    <v-btn depressed @click="refs.fileInput.click()">Choose a wav File</v-btn> +
                    
                    <span class ="file-cta">
                        <span class="file-icon">
                            <i class="fas fa-upload"></i>
                        </span>
                        <span class="file-label">
                            Choose a .wav file
                        </span>
                    </span>
                    

                </label>
                
            </div>
        </div> -->
        <div class="gen">
            <button class="button is-info">Send and Generate Audio</button>

            <!-- <button v-on:click="genAudio" class="button gen">Generate Audio!!</button> -->
        </div>

        <div id="dropzone">
            <vue-dropzone id="drop1" :options="dropOptions" ref="myVueDropzone"></vue-dropzone>
            
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
                :src = "showVisualizer"
                id = "audio" controls>
                audio element not supported
                <!-- "http://127.0.0.1:5000/api/getfile/new.wav"  -->
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
            <!-- <div class="dropzone">
                    <input 
                        type="file"
                        ref="file"
                        @change="selectFile" 
                        class="input-file"
                    />

                <p v-if="!uploading" class="call-to-action">
                    Drag your file here
                </p>
                <p v-if="uploading" class="progress-bar">

                </p>

            
             <label for="file" class="label">Upload File</label>
            <input type="file"
                ref="file"
                @change="selectFile"
            /> 

        </div> -->

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
// import VueAudio from 'vue-audio'
// import Vue from 'vue'
// Vue.use(AudioVisual)

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

            // audio: document.getElementById('audio'),
            // ctx: new AudioContext(),
            // analyser: this.ctx.createAnalyser(),
            // audioSrc: this.ctx.createMediaElementSource(audio),

            dzDisabled: false,
            dropOptions: {
                url: "http://127.0.0.1:5000/api/sendaudio",
                acceptedFiles: 'audio/wav',
                maxFilesize: 200,
                autoProcessQueue: false,
                // accept: function(file, done) {
                    
                // },
                // init: function() {
                //     this.on("addedfile", function(file) {document.getElementById("drop1").disabled; })
                // }
            }
        }
    },
    components: {
        vueDropzone,
        // 'vue-audio': VueAudio,
    },
    methods: {
        selectFile() {
            const file = this.$refs.file.files[0]
            const allowedTypes = ['audio/wav']
            const MAX_SIZE = 200000000
            const tooLarge = false//file.size > MAX_SIZE
            const filepath = ""

            if(allowedTypes.includes(file.type) && !tooLarge) {
                this.file = file // this.file.name
                this.filepath = "" 
                this.error = false
                this.msg = ""
                this.dzDisabled = true
                this.$refs.myVueDropzone.disableDropzone()
                console.log(file, this.dzDisabled)
                
            }
            else {
                this.error = true
                this.msg = tooLarge ? `File too large. Max Size is ${MAX_SIZE/100000}Mb`:"Only wav files are allowed"
                this.canGen = false
            }
        },
        async sendFile() {
            const formData = new FormData();
            this.file = this.$refs.myVueDropzone.getAcceptedFiles()[0]
            formData.append('file', this.file)
            try {
                // if we click send without having selected a file, 
                //console.log()
                // console.log(this.$refs.myVueDropzone.getAcceptedFiles())
                // console.log(this.$refs.myVueDropzone.processQueue())

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
                    // this.test()
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
        // test() {
        //     console.log('test')
        //     var audio = new Audio('http://127.0.0.1:5000/api/test');
        //     this.showVisualizer();
        // },
        playFile() {
            console.log('Playing audio')
            var audio = new Audio('http://127.0.0.1:5000/api/getfile/new.wav');
            this.showVisualizer()
            // audio.play();
        },
        genAudio() {
            if (this.canGen){
                console.log(this.filepath, 'filepath')
                const formData = new FormData();
                formData.append('filePath', this.filepath)
                formData.append('firstGen', this.firstGen)
                axios.post('http://127.0.0.1:5000/api/generate', formData)
                .then(response => {
                    //call playfile
                    this.firstGen = "2"
                    this.showVisualizer();
                })
            }
            if (!this.canGen){
                console.log(this.canGen)
            }
        },
        dzFileAdd() {
            // files = document.getElementById("drop1").getAcceptedFiles()
            // console.log(files)
        },
        showVisualizer() {
            // Credit to Cornelius Gee for the Visualizer code. https://codepen.io/cgyc8866/pen/wGRqLw
            console.log('visual');
            // document.getElementById("audiovis").style.left = "100px";
            // document.getElementById("audiovis").style.top  = "15px";
            
            var audio = document.getElementById('audio');
            console.log('var audioo');
            var ctx = new AudioContext();
            console.log('new ctx');
            audio.src = "http://127.0.0.1:5000/api/getfile/new.wav";
            console.log('src');
            var analyser = ctx.createAnalyser();
            console.log('made analyzer');
            var audioSrc = ctx.createMediaElementSource(audio);
            console.log('mediaelemsrc');
            
            // we have to connect the MediaElementSource with the analyser 
            audioSrc.connect(analyser); //breaks here on 2nd run 
            console.log('con audsrc');
            analyser.connect(ctx.destination);
            console.log('con analyze');
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
            this.reset(audioSrc, analyser, ctx, audio);
        },
        reset(audioSrc, analyser, ctx, audio) {
            console.log('resetting')
            this.$refs.myVueDropzone.enable()
            this.filepath = ""
            this.file = ""
            this.canGen = false
            console.log(this.file, this.filepath)
            audioSrc.disconnect();//analyser);
            analyser.disconnect();//ctx.destination);
            audio.src = "";
            ctx.close();
        }
        // initWebAudioApi () {
        //     // create a new audio context
        //     this.context = new (AudioContext || webkitAudioContext)();
        //     // bind the context to our <audio /> element
        //     this.source = this.context.createMediaElementSource(this.audio.base);
        // }
    },
    computed: {
        disableDropzone() {
            // if (dzDisabled) {
            //     document.getElementById("drop1").disabled = true;
            // } else {
            //     document.getElementById("drop1").disabled = false;
            // }
        },

        disableChooseButton () {

        },

        disableGenerate () {

        },
    },
    // mounted() {
    //     this.initWebAudioApi();
    // },
    
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
        /* position: relative; */
    }
    .dropzone {
        min-height: 150px;
        width: 80%;
        padding: 10px 10px;
        /* justify-content: center; */
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
        
        /* margin: 80px; */
        
        /* border: 4px solid goldenrod; */
    }
    .audio {
        justify-content: center;
        /* width: 80%; */
        /* margin: auto; */
        /* left: 40%; */
    }
    .canvas {
        position: absolute;
        justify-content: center;
        /* width: 80%; */
        /* margin: 0px 100px; */
        /* left: 40%; */
        z-index: 1;
    }

    .input-file {
        opacity: 0;
        width: 100px;
        height: 200px;
        position: absolute;
        cursor: pointer;
    }

    .dropzone.hover {
        color: rgb(21, 161, 207);
    }
    .gen{
        margin: auto;
        text-align: center;
        padding: 15px;
    }
    /* img.mainimg {
        height: 10%;
        width: 80%;
    } */

    /* body {
    background: #000;
    text-align: center;
    color: rgb(23, 168, 125);
    } */
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

</style>