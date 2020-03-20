<template>
    <div id="img-plus-info">

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
    </div>
</template>

<script>
export default {
    name: 'ImagePlusInfo',
    props: {
        msg: String,
    }
}
</script>