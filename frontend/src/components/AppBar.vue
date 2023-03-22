<template>
  <VAppBar app :color="isDark ? 'primary' : 'secondary'">
    <VToolbarTitle :class="
      isDark
        ? 'ml-3 mr-5 text-title text-amber'
        : 'ml-3 mr-5 text-title text-gray-700'
    ">
      ChatGPTVoice
    </VToolbarTitle>
  </VAppBar>
</template>