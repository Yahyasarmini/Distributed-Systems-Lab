import createShoppingService from '~/services/shopping';

export default ({ $axios }, inject) => {
  const shoppingService = createShoppingService($axios);
  inject('shoppingService', shoppingService);
};