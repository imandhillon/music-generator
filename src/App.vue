<template>

  <div id="app">
    <v-app>
      <v-content>
        <NavBar />
        <simple-upload />
      </v-content>
    </v-app>
  </div>

</template>

<script>
/* eslint-disable */
import HelloWorld from './components/HelloWorld';
import SimpleUpload from './components/SimpleUpload';
import NavBar from './components/NavBar';

export default {
  name: 'App',
  components: {
    HelloWorld,
    NavBar,
    SimpleUpload,
  },


  data: () => ({

  })
};
</script>
