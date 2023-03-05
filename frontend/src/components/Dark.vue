<template>
        <VBtn icon class="btn-circle tr fixed mt-20 mr-4" @click="toggleDark()"
        :class="!isDark ? 'bg-#03DAC6' : 'bg-#6200EE'"
        >
      <VIcon
      :class="isDark ? 'text-amber' : 'text-black'"
      >
        {{ isDark ? "mdi-white-balance-sunny" : "mdi-weather-night" }}
      </VIcon>
    </VBtn>
</template>