export default theme => ({
  divider: {
    backgroundColor: theme.grays.g0,
    marginTop: theme.spacing.unit * 2, // 16px
    marginBottom: theme.spacing.unit * 1,
  },
  header: {
    ...theme.typography.h4,
    color: theme.grays.g0
  },
  input: {
    color: theme.palette.primary.main
  },
  link: {
    color: theme.palette.secondary.main
  },
  text: {
    color: theme.grays.g0
  }
});