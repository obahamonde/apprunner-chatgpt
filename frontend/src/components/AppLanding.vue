<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue"
const { loginWithRedirect } = useAuth0()
</script>

<template>
    <VCard class="col center p-8 shadow-black shadow-lg bg-gray-500 rounded-lg">
     <h1 class="text-cyan text-4xl font-sans m-4">Welcome to ChatGPT7</h1>
    <img src="/logo.svg" class="rf x6 m-4 cp scale hover:animate-spin"/>
    <h1 class="text-white text-2xl font-mono m-4">Press the button below to Continue</h1>
    <button class="m-4 btn-post" @click="loginWithRedirect()">Get Started</button>
</VCard>
</template>