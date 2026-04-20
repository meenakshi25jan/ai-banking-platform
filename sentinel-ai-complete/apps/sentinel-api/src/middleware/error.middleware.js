export function errorHandler(error, _req, res, _next) {
  console.error(error);
  return res.status(500).json({
    error: 'Internal Server Error',
    message: error.message
  });
}
