Вот модифицированный код без комментариев с добавлением функционала для отображения описания курса:

```vue
<template>
  <div class="surface-ground p-3 lg:p-4">
    <Toast/>
    <div v-if="loading" class="p-d-flex p-jc-center p-ai-center" style="min-height: 300px;">
      <ProgressSpinner animationDuration=".5s"/>
    </div>
    <div v-else class="surface-card shadow-2 p-4 lg:p-5 border-round">
      <div class="flex justify-content-between align-items-center mb-5 flex-wrap gap-3">
        <div class="flex align-items-center">
          <Avatar :label="userInitials" size="xlarge" shape="circle" class="mr-3 flex-shrink-0"
                  :style="{ backgroundColor: getAvatarColor(user.id), color: '#ffffff' }"/>
          <div>
            <h1 class="text-3xl mb-1">{{ fullName }}</h1>
            <div class="flex align-items-center text-600 mt-1">
              <i class="pi pi-envelope mr-2"></i>
              <span>{{ user.email || 'Email не указан' }}</span>
            </div>
            <div class="flex align-items-center text-600 mt-1">
              <i class="pi pi-map-marker mr-2"></i>
              <span v-if="userInfo && !isEditing">{{
                  userInfo.city || 'Город не указан'
                }}, {{ userInfo.country || 'Страна не указана' }}</span>
              <span v-else-if="!userInfo && !isEditing">Местоположение не указано</span>
            </div>
          </div>
        </div>
        <div class="flex gap-2">
          <Button v-if="!isEditing && userInfo" label="Редактировать профиль" icon="pi pi-pencil" @click="startEdit"/>
          <Button v-else-if="isEditing" label="Сохранить" icon="pi pi-check" class="p-button-success"
                  @click="saveProfile" :loading="saving"/>
          <Button v-if="isEditing" label="Отмена" icon="pi pi-times" class="p-button-secondary" @click="cancelEdit"/>
          <Button v-if="!userInfo && !isEditing" label="Заполнить профиль" icon="pi pi-user-edit" @click="startEdit"
                  class="p-button-info"/>
        </div>
      </div>

      <div v-if="isEditing" class="mb-5 surface-100 border-round p-4">
        <h3 class="mt-0 mb-4">Редактирование профиля</h3>
        <div class="grid formgrid">
          <div class="field align-items-center gap-2 col-12 md:col-6">
            <label for="surname" class="block text-900 font-medium mb-2">Фамилия</label>
            <InputText id="surname" v-model="editableUserInfo.surname" class="w-full"/>
          </div>
          <div class="field align-items-center gap-2 col-12 md:col-6">
            <label for="middlename" class="block text-900 font-medium mb-2">Отчество</label>
            <InputText id="middlename" v-model="editableUserInfo.middlename" class="w-full"/>
          </div>
          <div class="field align-items-center gap-2 col-12 md:col-6">
            <label for="edit-city" class="block text-900 font-medium mb-2">Город</label>
            <InputText id="edit-city" v-model="editableUserInfo.city" class="w-full"/>
          </div>
          <div class="field align-items-center gap-2 col-12 md:col-6">
            <label for="edit-country" class="block text-900 font-medium mb-2">Страна</label>
            <InputText id="edit-country" v-model="editableUserInfo.country" class="w-full"/>
          </div>
          <div class="field align-items-center gap-2 col-12 md:col-6">
            <label for="gender" class="block text-900 font-medium mb-2">Пол</label>
            <Dropdown id="gender" v-model="editableUserInfo.gender" :options="genderOptions" optionLabel="label"
                      optionValue="value" placeholder="Выберите пол" class="w-full"/>
          </div>
          <div class="field col-12 md:col-6">
            <label for="dob" class="block text-900 font-medium mb-2">Дата рождения</label>
            <Calendar id="dob" v-model="editableUserInfo.dd_mm_yy_date" dateFormat="yy-mm-dd" placeholder="ГГГГ-ММ-ДД"
                      :showIcon="true" class="w-full"/>
          </div>
        </div>
      </div>
      <Message v-if="!userInfo && !isEditing" severity="warn" :closable="false" class="mb-4">
        Ваш профиль не полностью заполнен. Нажмите "Заполнить профиль", чтобы добавить дополнительную информацию.
      </Message>

      <div class="grid mb-4">
        <div class="col-12 md:col-6">
          <Card class="h-full">
            <template #title>Подтвержденные навыки</template>
            <template #content>
              <div v-if="skills.length === 0" class="text-center text-600 p-3">У вас пока нет подтвержденных навыков.
              </div>
              <div v-else>
                <div v-for="skill in skills" :key="skill.id" class="mb-4">
                  <div class="flex justify-content-between align-items-center mb-1 flex-wrap gap-2">
                    <div class="flex align-items-center gap-2">
                      <span class="font-medium">{{ skill.skill_name }}</span>
                      <Tag :value="skill.type === true ? 'Hard' : 'Soft'"
                           :severity="skill.type === true ? 'primary' : 'success'"
                           :icon="skill.type === true ? 'pi pi-cog' : 'pi pi-user'"/>
                    </div>
                    <Tag :value="skill.category || 'Без категории'" severity="info" icon="pi pi-tag"/>
                  </div>
                  <div class="flex w-full align-items-center justify-content-between gap-2 mt-2">
                    <span class="text-sm">Уровень {{ skill.level }}/{{ MAX_SKILL_LEVEL }}</span>
                    <Button
                        v-if="skill.level < MAX_SKILL_LEVEL"
                        label="Пройти заново"
                        icon="pi pi-refresh"
                        class="p-button-sm"
                        @click="reconfirmSkill(skill)"
                    />
                    <span v-else class="text-sm text-green-600 font-medium">
                      <i class="pi pi-check-circle mr-1"></i>Макс. уровень
                    </span>
                  </div>
                  <ProgressBar class="mt-2" :value="(skill.level / MAX_SKILL_LEVEL) * 100" :showValue="false"
                               style="height: 6px"/>
                </div>
              </div>
            </template>
          </Card>
        </div>

        <div class="col-12 md:col-6">
          <Card class="h-full">
            <template #title>Доступные навыки</template>
            <template #content>
              <div v-if="availableSkills.length === 0" class="text-center text-600 p-3">Нет навыков для подтверждения.
              </div>
              <div v-else>
                <div v-for="skill in availableSkills" :key="skill.id" class="mb-3 border-bottom-1 surface-border pb-2">
                  <div class="flex justify-content-between align-items-center flex-wrap gap-2">
                    <div class="flex align-items-center gap-2">
                      <span class="font-medium">{{ skill.skill_name }}</span>
                      <Tag :value="skill.type === true ? 'Hard' : 'Soft'"
                           :severity="skill.type === true ? 'primary' : 'success'"
                           :icon="skill.type === true ? 'pi pi-cog' : 'pi pi-user'"/>
                      <Tag :value="skill.category || 'Без категории'" severity="info" icon="pi pi-tag"/>
                    </div>
                    <Button label="Подтвердить" icon="pi pi-check" class="p-button-sm" @click="confirmSkill(skill)"/>
                  </div>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </div>

      <div class="col-12 mt-3">
        <Card>
          <template #title>Рекомендуемые курсы</template>
          <template #content>
            <div v-if="courses.length === 0" class="text-center text-600">Рекомендуемых курсов пока нет.</div>
            <div v-else class="grid">
              <div v-for="course in courses" :key="course.id" class="col-12 md:col-6 lg:col-4">
                <div class="border-round surface-border border-1 h-full w-full flex flex-column p-3">
                  <h3 class="text-xl mt-0 mb-2">{{ course.name }}</h3>
                  <div class="flex justify-content-between mb-3 text-sm text-600">
                    <Tag :value="'Сложность: ' + course.difficulty" severity="warning"/>
                    <Tag :value="course.duration_hrs + ' часов'" icon="pi pi-clock" severity="info"/>
                  </div>
                  <p class="line-height-3 text-sm flex-grow-1">{{ course.description }}</p>
                  <Button label="Подробнее" class="mt-3 p-button-sm" @click="showCourseDetails(course)"/>
                </div>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <Dialog v-model:visible="courseDialogVisible" :style="{width: '50vw'}" header="Описание курса">
      <div v-if="selectedCourse">
        <h3 class="mt-0">{{ selectedCourse.name }}</h3>
        <div class="flex gap-2 mb-4">
          <Tag :value="'Сложность: ' + selectedCourse.difficulty" severity="warning"/>
          <Tag :value="selectedCourse.duration_hrs + ' часов'" icon="pi pi-clock" severity="info"/>
        </div>
        <p class="line-height-3">{{ selectedCourse.description }}</p>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import api from '../utils/api';
import Avatar from 'primevue/avatar';
import ProgressBar from 'primevue/progressbar';
import Tag from 'primevue/tag';
import Card from 'primevue/card';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Calendar from 'primevue/calendar';
import Dropdown from 'primevue/dropdown';
import Message from 'primevue/message';
import ProgressSpinner from 'primevue/progressspinner';
import Toast from 'primevue/toast';
import Dialog from 'primevue/dialog';
import {useToast} from 'primevue/usetoast';

const router = useRouter();
const toast = useToast();
const loading = ref(true);
const saving = ref(false);
const user = ref({});
const userInfo = ref(null);
const editableUserInfo = ref({});
const skills = ref([]);
const allSkills = ref([]);
const courses = ref([]);
const isEditing = ref(false);
const MAX_SKILL_LEVEL = 10;
const courseDialogVisible = ref(false);
const selectedCourse = ref(null);

const genderOptions = ref([
  {label: 'Мужской', value: true},
  {label: 'Женский', value: false}
]);

const userSkillsIds = computed(() => skills.value.map(skill => skill.skill_id));

const availableSkills = computed(() =>
    allSkills.value.filter(skill => !userSkillsIds.value.includes(skill.id))
);

const userInitials = computed(() => {
  const firstName = user.value.first_name;
  const lastName = userInfo.value?.surname;
  if (firstName && lastName) return `${firstName[0]}${lastName[0]}`.toUpperCase();
  if (firstName) return firstName[0].toUpperCase();
  if (user.value.username) return user.value.username[0].toUpperCase();
  return '??';
});

const fullName = computed(() => {
  const firstName = user.value.first_name;
  const lastName = userInfo.value?.surname;
  if (firstName && lastName) return `${firstName} ${lastName}`;
  if (firstName) return firstName;
  return user.value.username || 'Пользователь';
});

const parseDate = (dateString) => {
  if (!dateString) return null;
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? null : date;
};

const formatDateForSave = (dateObject) => {
  if (!dateObject || !(dateObject instanceof Date)) return null;
  return dateObject.toISOString().split('T')[0];
};

const loadData = async () => {
  loading.value = true;
  userInfo.value = null;
  skills.value = [];
  try {
    const userRes = await api.get('/auth/users/me/');
    user.value = userRes.data;
    if (!user.value.id) throw new Error("ID пользователя не найден.");

    try {
      const formsRes = await api.get('/form/');
      userInfo.value = formsRes.data.find(form => form.user_id === user.value.id) || null;
    } catch (formError) {
      userInfo.value = null;
    }

    const coursesRes = await api.get('/cources/');
    courses.value = coursesRes.data;

    const skillsListRes = await api.get('/skills/');
    allSkills.value = skillsListRes.data;
    const skillsMap = Object.fromEntries(allSkills.value.map(skill => [skill.id, skill]));

    try {
      const userSkillsRes = await api.get('/user-skill/', {params: {user: user.value.id}});
      skills.value = userSkillsRes.data.map(us => ({
        ...us,
        skill_name: skillsMap[us.skill_id]?.skill_name || '?',
        category: skillsMap[us.skill_id]?.category || '?',
        type: skillsMap[us.skill_id]?.type ?? false
      }));
    } catch (userSkillError) {
      const allUserSkillsRes = await api.get('/user-skill/');
      skills.value = allUserSkillsRes.data
          .filter(us => us.user_id === user.value.id)
          .map(us => ({
            ...us,
            skill_name: skillsMap[us.skill_id]?.skill_name || '?',
            category: skillsMap[us.skill_id]?.category || '?',
            type: skillsMap[us.skill_id]?.type ?? false
          }));
    }
  } catch (error) {
    toast.add({severity: 'error', summary: 'Ошибка загрузки', detail: 'Не удалось загрузить данные.', life: 4000});
  } finally {
    loading.value = false;
  }
};

const startEdit = () => {
  editableUserInfo.value = userInfo.value
      ? {...userInfo.value, dd_mm_yy_date: parseDate(userInfo.value.dd_mm_yy)}
      : {surname: '', middlename: '', city: '', country: '', gender: null, dd_mm_yy_date: null};
  isEditing.value = true;
};

const saveProfile = async () => {
  saving.value = true;
  try {
    const payload = {
      ...editableUserInfo.value,
      user_id: user.value.id,
      dd_mm_yy: formatDateForSave(editableUserInfo.value.dd_mm_yy_date)
    };
    delete payload.dd_mm_yy_date;
    delete payload.form_id;

    let response;
    if (userInfo.value?.form_id) {
      response = await api.put(`/form/${userInfo.value.form_id}/`, payload);
    } else {
      response = await api.post('/form/', payload);
    }
    userInfo.value = {...response.data};
    isEditing.value = false;
    toast.add({severity: 'success', summary: 'Успешно', detail: 'Профиль сохранен', life: 3000});
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Ошибка сохранения',
      detail: `${error.response?.data?.detail || JSON.stringify(error.response?.data) || error.message}`,
      life: 5000
    });
  } finally {
    saving.value = false;
  }
};

const cancelEdit = () => {
  isEditing.value = false;
};

const confirmSkill = (skill) => {
  router.push(`/test/${skill.id}`);
};

const reconfirmSkill = (userSkill) => {
  if (userSkill.level < MAX_SKILL_LEVEL) {
    router.push(`/retest/${userSkill.skill_id}`);
  } else {
    toast.add({
      severity: 'info',
      summary: 'Информация',
      detail: 'Максимальный уровень этого навыка уже достигнут.',
      life: 3000
    });
  }
};

const showCourseDetails = (course) => {
  selectedCourse.value = course;
  courseDialogVisible.value = true;
};

const stringHashCode = (str) => {
  let hash = 0;
  if (!str || str.length === 0) return hash;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return hash;
};

const getAvatarColor = (userId) => {
  if (!userId) return '#dee2e6';
  const colors = ['#0D9276', '#40A578', '#9DDE8B', '#1B4242', '#5C8374', '#93B1A6', '#FF6B6B', '#E6FF94'];
  const index = Math.abs(stringHashCode(String(userId))) % colors.length;
  return colors[index];
};

onMounted(loadData);
</script>

<style scoped>
.p-avatar {
  background-color: var(--primary-color);
  color: var(--primary-color-text);
  flex-shrink: 0;
}

.p-field > label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.h-full {
  height: 100%;
}

.w-full {
  width: 100%;
}

/* Styles for grid and cards to ensure consistent height */
.grid > .col-12, .grid > .md\:col-6 { /* Target columns directly under .grid */
  display: flex;
}

.grid > .col-12 > .p-card, .grid > .md\:col-6 > .p-card { /* Target cards directly under those columns */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.grid > .col-12 > .p-card > .p-card-content, .grid > .md\:col-6 > .p-card > .p-card-content {
  flex-grow: 1; /* Allow content to take remaining space */
}

/* Styles for the course grid *inside* the main card */
.col-12 > .p-card .grid > .col-12,
.col-12 > .p-card .grid > .md\:col-6, /* Use escaped colon for md:col-6 */
.col-12 > .p-card .grid > .lg\:col-4 { /* Use escaped colon for lg:col-4 */
  display: flex; /* Ensure course cards use flex */
}
</style>