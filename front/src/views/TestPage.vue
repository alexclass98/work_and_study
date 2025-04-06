<template>
  <div class="p-4 surface-card shadow-2 border-round">
    <div v-if="loading" class="p-d-flex p-jc-center p-p-5">
      <ProgressSpinner animationDuration=".5s"/>
    </div>
    <div v-else-if="skill && skill.id">
      <h1 class="text-3xl font-bold mb-3">{{ skill.skill_name }}</h1>

      <div class="flex align-items-center gap-2 mb-3">
        <Tag
            :value="skill.type === true ? 'Hard' : 'Soft'"
            :severity="skill.type === true ? 'primary' : 'success'"
            :icon="skill.type === true ? 'pi pi-cog' : 'pi pi-user'"
        />
        <Tag :value="skill.category || 'Без категории'" severity="info" icon="pi pi-tag" />
      </div>

      <p class="text-lg">{{ skill.description || 'Описание отсутствует' }}</p>

      <!-- Кнопка "Начать" которая просто показывает секцию теста/завершения -->
      <Button label="Начать тестирование" icon="pi pi-play" class="mt-4 p-button-lg" @click="toggleTest" v-if="!showTest"/>

      <!-- Контейнер для теста (показывается после нажатия "Начать") -->
      <div v-if="showTest" class="mt-4">
        <h2 class="text-2xl font-bold mb-2">Прохождение теста</h2>
        <iframe v-if="skill.test" :src="skill.test" class="test-iframe border-round shadow-1"></iframe>
        <p v-else class="text-lg text-center">Ссылка на тест отсутствует</p>
      </div>

      <!-- Кнопка завершить тест (показывается после нажатия "Начать") -->
      <div v-if="showTest" class="mt-4">
        <Button
            label="Завершить (Подтвердить Уровень 1)"
            icon="pi pi-check"
            class="p-button-success"
            @click="completeTest"
            :loading="submitting"
            :disabled="submitting"
        />
      </div>
    </div>
    <div v-else class="text-center text-600 p-5">
      Не удалось загрузить информацию о навыке.
    </div>
    <Toast />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../utils/api';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import ProgressSpinner from 'primevue/progressspinner';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const skill = ref({});
const user = ref(null);
const loading = ref(true);
const submitting = ref(false);
const showTest = ref(false); // Вернули для исходной логики показа/скрытия
const MAX_SKILL_LEVEL = 10;

const loadSkillAndUser = async () => {
  loading.value = true;
  skill.value = {};
  user.value = null;
  try {
    const [userResponse, skillResponse] = await Promise.all([
      api.get('/auth/users/me/').catch(err => { console.error('Не удалось получить пользователя:', err); return null; }),
      api.get(`/skills/${route.params.id}/`).catch(err => { console.error('Ошибка загрузки навыка:', err); return null; })
    ]);
    if (userResponse) user.value = userResponse.data;
    if (skillResponse) skill.value = skillResponse.data;

    if(user.value && skill.value) {
      try {
        const userSkillRes = await api.get('/user-skill/', { params: { user: user.value.id, skill: skill.value.id } });
        if (userSkillRes.data && userSkillRes.data.length > 0) {
          toast.add({ severity: 'info', summary: 'Информация', detail: 'Вы уже подтвердили этот навык.', life: 4000 });
          // router.push('/profile'); // Можно раскомментировать для редиректа
        }
      } catch (e) { /* Ошибка 404 ожидаема */ }
    }

  } catch (error) {
    console.error("Ошибка при загрузке:", error);
    toast.add({ severity: 'error', summary: 'Ошибка загрузки', detail: 'Произошла ошибка.', life: 4000 });
  } finally {
    loading.value = false;
  }
};

const toggleTest = () => {
  showTest.value = !showTest.value;
};

const completeTest = async () => {
  if (!user.value?.id || !skill.value?.id) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Необходимые данные отсутствуют.', life: 3000 });
    return;
  }
  submitting.value = true;
  try {
    const startLevel = 1;
    const payload = {
      user_id: user.value.id,
      skill_id: skill.value.id,
      level: startLevel,
    };
    await api.post('/user-skill/', payload);
    toast.add({ severity: 'success', summary: 'Успешно', detail: `Навык "${skill.value.skill_name}" подтвержден (Уровень ${startLevel}).`, life: 3000 });
    router.push('/profile');
  } catch (error) {
    console.error('Ошибка подтверждения навыка:', error);
    let errorMsg = 'Произошла ошибка при подтверждении.';
    if (error.response?.status === 400 && error.response?.data) {
      let detail = JSON.stringify(error.response.data);
      if (typeof error.response.data === 'object') {
        detail = Object.values(error.response.data).flat().join(' ') || detail;
      }
      errorMsg = `Не удалось подтвердить. Возможно, навык уже добавлен. (${detail})`;
    } else if (error.message) {
      errorMsg = `Произошла ошибка: ${error.message}`;
    }
    toast.add({ severity: 'error', summary: 'Ошибка', detail: errorMsg, life: 5000 });
  } finally {
    submitting.value = false;
  }
};

onMounted(loadSkillAndUser);
</script>

<style scoped>
.test-iframe {
  width: 80%;
  height: 600px;
  border: none;
  transform: scale(0.8);
  transform-origin: 0 0;
  pointer-events: auto;
  overflow: hidden;
}
</style>