<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { isAuthenticated, loginWithRedirect } = useAuth0();
</script>
<template>
  <div v-if="isAuthenticated">
    <VApp app>
      <RouterView />
    </VApp>
  </div>
  <div v-else col center p-12 bg-gray-700 h-screen>
    <AppLanding />
</div>
</template>
