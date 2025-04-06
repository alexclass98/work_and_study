<template>
  <div class="p-4 surface-card shadow-2 border-round">
    <div v-if="loading" class="p-d-flex p-jc-center p-p-5">
      <ProgressSpinner animationDuration=".5s"/>
    </div>
    <div v-else-if="skill && skill.id && userSkill">
      <h1 class="text-3xl font-bold mb-3">{{ skill.skill_name }}</h1>
      <div class="flex align-items-center gap-2 mb-3">
        <Tag :value="skill.type === true ? 'Hard' : 'Soft'" :severity="skill.type === true ? 'primary' : 'success'" :icon="skill.type === true ? 'pi pi-cog' : 'pi pi-user'"/>
        <Tag :value="skill.category || 'Без категории'" severity="info" icon="pi pi-tag" />
      </div>
      <p class="text-lg">{{ skill.description || 'Описание отсутствует' }}</p>

      <!-- Отображаем текущий уровень -->
      <div class="mt-4">
        <p class="text-lg">Текущий уровень: {{ userSkill.level }} / {{ MAX_SKILL_LEVEL }}</p>
        <ProgressBar :value="(userSkill.level / MAX_SKILL_LEVEL) * 100" :showValue="false" style="height: 8px"/>
        <p v-if="userSkill.level >= MAX_SKILL_LEVEL" class="mt-2 text-green-600 font-medium">
          <i class="pi pi-check-circle mr-1"></i> Максимальный уровень достигнут!
        </p>
      </div>

      <!-- Кнопка "Пройти заново" для показа теста -->
      <Button
          v-if="userSkill.level < MAX_SKILL_LEVEL"
          label="Пройти заново"
          icon="pi pi-refresh"
          class="mt-4 p-button-lg"
          @click="toggleTest"
      />

      <!-- Контейнер для теста -->
      <div v-if="showTest" class="mt-4">
        <h2 class="text-2xl font-bold mb-2">Прохождение теста</h2>
        <iframe v-if="skill.test" :src="skill.test" class="test-iframe border-round shadow-1"></iframe>
        <p v-else class="text-lg text-center">Ссылка на тест отсутствует</p>
      </div>

      <!-- Кнопка завершить тест (для повышения уровня) -->
      <div v-if="showTest && userSkill.level < MAX_SKILL_LEVEL" class="mt-4">
        <Button
            label="Завершить и повысить уровень"
            icon="pi pi-check"
            class="p-button-success"
            @click="recompleteTest"
            :loading="submitting"
            :disabled="submitting"
        />
      </div>
    </div>
    <div v-else class="text-center text-600 p-5">
      Не удалось загрузить информацию или вы еще не подтвердили этот навык.
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
import ProgressBar from 'primevue/progressbar';
import ProgressSpinner from 'primevue/progressspinner';
import Message from 'primevue/message';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const skill = ref({});
const showTest = ref(false);
const userSkill = ref(null);
const user = ref({});
const loading = ref(true);
const submitting = ref(false);
const MAX_SKILL_LEVEL = 10;

const loadData = async () => {
  loading.value = true;
  skill.value = {};
  user.value = {};
  userSkill.value = null;
  let currentUserId = null;
  let currentSkillId = route.params.id;

  try {
    const responseUser = await api.get('/auth/users/me/');
    if (!responseUser.data?.id) throw new Error('Не удалось получить пользователя');
    user.value = responseUser.data;
    currentUserId = user.value.id;

    const responseSkill = await api.get(`/skills/${currentSkillId}/`);
    if (!responseSkill.data?.id) throw new Error('Не удалось получить навык');
    skill.value = responseSkill.data;

    const responseUserSkill = await api.get(`/user-skill/`, {
      params: { user_id: currentUserId, skill_id: currentSkillId }
    });
    if (responseUserSkill.data?.length > 0) {
      userSkill.value = responseUserSkill.data[0];
    } else {
      throw new Error('Запись о навыке пользователя не найдена.');
    }

  } catch (error) {
    console.error('Ошибка загрузки данных для пересдачи:', error);
    toast.add({ severity: 'error', summary: 'Ошибка', detail: `Не удалось загрузить данные: ${error.message}`, life: 5000 });
  } finally {
    loading.value = false;
  }
};

const toggleTest = () => {
  showTest.value = !showTest.value;
};

const recompleteTest = async () => {
  if (!userSkill.value || !user.value?.id || !skill.value?.id) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Отсутствуют необходимые данные.', life: 3000 });
    return;
  }
  if (userSkill.value.level >= MAX_SKILL_LEVEL) {
    toast.add({ severity: 'info', summary: 'Информация', detail: 'Максимальный уровень уже достигнут.', life: 3000 });
    return;
  }
  submitting.value = true;
  try {
    const newLevel = Math.min(userSkill.value.level + 1, MAX_SKILL_LEVEL);
    const payload = {
      user_id: user.value.id,
      skill_id: skill.value.id,
      level: newLevel,
    };
    await api.put(`/user-skill/${userSkill.value.id}/`, payload);
    toast.add({ severity: 'success', summary: 'Успех!', detail: `Уровень навыка "${skill.value.skill_name}" повышен до ${newLevel}.`, life: 3000 });
    router.push('/profile');
  } catch (error) {
    console.error('Ошибка обновления уровня навыка:', error);
    toast.add({ severity: 'error', summary: 'Ошибка', detail: `Не удалось обновить уровень: ${error.response?.data?.detail || error.message}`, life: 5000 });
  } finally {
    submitting.value = false;
  }
};

onMounted(loadData);
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