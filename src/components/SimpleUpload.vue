<template>
    <form @submit.prevent="sendFile" enctype="multipart/form-data">

    <div v-if="msg"
        :class="`msg ${error ? 'is-danger' : 'is-success'}`" >
        <div class="msg-body">{{msg}}
        </div>
    </div>

        <div class="field">

            <div class="file is boxed is-primary">
                <label class="file-label">

                    <input type="file"
                        ref="file"
                        @change="selectFile"
                        class="file-input"
                    />
                    <!-- <v-btn depressed @click="refs.fileInput.click()">Choose a wav File</v-btn> -->
                    
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
        </div>
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

        <div class="field">
            <button class="button is-info">Send</button>

            <button v-on:click="genAudio" class="button gen">Generate Audio!!</button>
        </div>




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

        </div> comment?-->


        
    </form>

    


</template>

<script>
/* eslint-disable */
import axios from 'axios'
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
            isDisabled: true,
            filepath: ""
        }
    },
    methods: {
        selectFile() {
            const file = this.$refs.file.files[0]
            const allowedTypes = ['audio/wav', 'text/plain']
            const MAX_SIZE = 200000000
            const tooLarge = false//file.size > MAX_SIZE
            const filepath = ""

            if(allowedTypes.includes(file.type) && !tooLarge) {
                this.file = file // this.file.name
                this.filepath = "" 
                this.error = false
                this.msg = ""
                console.log(file)
            }
            else {
                this.error = true
                this.msg = tooLarge ? `File too large. Max Size is ${MAX_SIZE/100000}Mb`:"Only wav files are allowed"
                this.canGen = false
            }
        },
        async sendFile() {
            const formData = new FormData();
            formData.append('file', this.file)
            try {
                // try to accesss file elem here to trigger error if bad
                console.log()
                await axios.post("http://127.0.0.1:5000/api/sendaudio", formData)
                .then(response => {
                    this.filepath = response.data.uploadPath
                    console.log(this.filepath)
                    this.canGen = true

                    this.msg = "File uploaded"
                    this.file = ""
                    this.error = false
                })
                .catch(error => {
                    console.log(error)
                })
                
            }
            catch(err) {
                this.msg = err.response.data.error
                this.error = true
            }
        },
        playFile() {
            console.log('hi')
            var audio = new Audio('http://127.0.0.1:5000/api/getfile/new.wav'); // response.file or smth
            audio.play();

            // axios.get('http://127.0.0.1:5000/api/getfile/new.wav', {
            //     responseType: 'blob',
            // })
            // .then(response => {
            //     console.log(response)
            //     var audio = new Audio(response.data); // response.file or smth
            //     audio.play();
            // })
        },
        genAudio() {
            if (this.canGen){
                console.log(this.filepath, '111')
                const formData = new FormData();
                formData.append('filePath', this.filepath)
                axios.post('http://127.0.0.1:5000/api/generate', formData)
                .then(response => {
                    //call playfile
                    this.playFile();
                    var musicPath = ""
                    var musicTemp = response.data.wavPath
                    var musicTemp = musicPath.concat("file://", musicTemp);
                    console.log(musicTemp)

                    // var audio = new Audio(musicTemp); // path to file
                    // audio.play();
                })
            }
            if (!this.canGen){
                console.log(this.canGen)
            }
        }
    }
}
</script>


<style scoped>
    .dropzone {
        min-height: 200px;
        padding: 10px 10px;
        position: relative;
        cursor: pointer;
        outline: 2px dashed grey;
        outline-offset: -10px;
        background: lightcyan;
        color: dimgray;
    }

    .input-file {
        opacity: 0;
        width: 100px;
        height: 200px;
        position: absolute;
        cursor: pointer;
    }

    .dropzone.hover {
        color: lightblue;
    }

</style>