<script setup lang="ts">
//Importing dependencies
import { useAuth0 } from "@auth0/auth0-vue";
import { Message, User, useSpeech } from "../hooks";
import { useSynthesis } from '../hooks/synthesis';
const { state, notify } = useStore();
const { text, play } = useSynthesis();

//Using auth0
const {
  isAuthenticated,
  getAccessTokenSilently,
  user,
  logout,
  loginWithRedirect,
} = useAuth0();

//Declaring the query parameter
const q = ref("");

//Using the speech recognition hook
const { speech, result, isListening } = useSpeech()

//Speech recognition composed functions
const startSpeech = () => {
  q.value = "";
  isListening.value = true;
  speech.start();
};
const stopSpeech = ()=>{
  q.value = result.value;
  if (!q.value.length) return false;
  speech.stop();
  isListening.value = false;
  return true;
}

//Getting user info from the API
const getUserInfo = async() =>{
  if (state.user) return;
  const token = await getAccessTokenSilently();
    const { data } = await useFetch(
      `/api/auth?token=${token}`
    ).json();
    state.user = unref(data) as User;
    notify({
      message: `Welcome ${state.user.name}`,
      status: "success",
    });
}

//Getting Completions from the API
const getCompletion = async()=>{
  const { data } = await useFetch(
    `api/completion?q=${q.value}&sub=${user.value.sub}&tokens=128`,
    {
      method: "GET",
    }
  ).text();
  q.value = "";
  const characters = unref(data) as string;
  state.messages.unshift({
    message: "",
    sender: "bot",
    created_at: new Date().toLocaleTimeString(),
  });
  text.value = characters;
  play();
  for (let i = 0; i < characters.length; i++) {
    state.messages[0]["message"] += characters[i];
    await new Promise((resolve) => setTimeout(resolve, 50));
    
  }
}

//Pushing the message to the state
const pushMessage = ()=>{
  if (!q.value.length) return;
  state.messages.unshift({
    message: q.value,
    sender: "user",
    created_at: new Date().toLocaleString(),
  });
}

//Sending the message to the API
const sendText = async () => {
  pushMessage();
  await getCompletion();
};

//Sending the speech to the API
const sendSpeech = async () => {
  const c = stopSpeech();
  if (!c) {
    notify({
      message: "We couldn't hear you, please check your microphone or type your message",
      status: "error",
    });
    isListening.value = false;
    return;
  }
  await sendText();
  result.value = "";
};

//Fetching historical messages from the API
const fetchMessages = async () => {
  if (state.messages.length) return;
  const { data } = await useFetch(
    `/api/chats?sub=${user.value.sub}`
  ).json();
  const response = unref(data) as Message[]
  if (!response.length) return;
  response.forEach((msg: Message) => {
    msg.created_at = new Date(msg.created_at).toLocaleString();
    state.messages.unshift(msg);
  });
 notify({
    message:`You have ${response.length} messages in your history`,
    status:"info"
  })
};

//OnMounted hook
onMounted(async () => {
  if (isAuthenticated.value) {
    await getUserInfo();
    await fetchMessages();
  } else {
    await loginWithRedirect();
  }
});
</script>
<template>
    <VFooter
    app
    class="row center"
    :class="isDark ? 'bg-primary' : 'bg-secondary'"
  >
    <img
      class="rf sh x4"
      :src="
        user.picture
          ? user.picture
          : 'https://media.istockphoto.com/id/1167753373/vector/woman-avatar-isolated-on-white-background-vector-illustration-for-your-design.jpg'
      "
    />
    <Icon
      icon="mdi-microphone"
      text-xl
      text-accent
      cp scale
      dark:text-cyan
      v-if="!isListening"
      @click="startSpeech"
    />
    <Icon
      icon="mdi-microphone-off"
      text-xl
      text-secondary
      cp scale
      dark:text-primary
      v-else
      @click="sendSpeech"
    />
    <VTextField
      v-model="q"
      :label="user.name"
      placeholder="Ask anything to ChatGPT"
      outlined
      dense
      rounded
      class="ml-3"
      @keydown.enter="sendText"
    />
    <VBtn
      title="Logout"
      :class="
        isDark
          ? 'bg-red-500 ml-3 text-white scale cp'
          : 'bg-red-700 ml-3 text-white scale cp'
      "
      @click="logout()"
      icon
    >
      <VIcon>mdi-logout </VIcon>
    </VBtn>
  </VFooter>
</template>