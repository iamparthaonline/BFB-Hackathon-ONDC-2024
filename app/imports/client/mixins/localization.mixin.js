import Vue from 'vue';
import en from '../i18n/en.json';
import mr from '../i18n/mr.json';
import gu from '../i18n/gu.json';
import ta from '../i18n/ta.json';
import kn from '../i18n/kn.json';

const locales = {
  en,
  mr,
  gu,
  ta,
  kn,
};

const state = Vue.observable({
  locale: 'en',
  translations: locales.en,
});

const loadLocale = locale => {
  console.log(locale, 'locale');
  if (locales[locale]) {
    state.translations = locales[locale];
    state.locale = locale;
  } else {
    console.error(`Locale ${locale} not found`);
  }
};

const setLocalStorage = () => {
  if (localStorage.getItem('language')) {
    loadLocale(localStorage.getItem('language'));
  }
};

const translate = key => {
  return state.translations[key] || key;
};

export default {
  data() {
    return {
      localeState: state,
    };
  },
  methods: {
    _(key) {
      return translate(key);
    },
    setLocale(locale) {
      loadLocale(locale);
      localStorage.setItem('language', locale);
    },
  },
};

loadLocale(state.locale);
setLocalStorage();