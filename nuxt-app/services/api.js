export default ($axios) => ({
    fetchExamples() {
      return $axios.$get('/examples');
    },
    createExample(data) {
      return $axios.$post('/examples', data);
    },
  });
  