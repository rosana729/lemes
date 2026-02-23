<?php

namespace App\Util;

use Symfony\Component\HttpFoundation\JsonResponse;

/**
 * Utilidad de Respuestas
 * 
 * Formatea todas las respuestas API de manera consistente
 */
class ResponseUtil
{
    /**
     * Respuesta exitosa
     */
    public static function success($data, int $status = 200): JsonResponse
    {
        return new JsonResponse([
            'success' => true,
            'data' => $data
        ], $status, [
            'Access-Control-Allow-Origin' => '*',
            'Access-Control-Allow-Methods' => 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers' => 'Content-Type, Authorization'
        ]);
    }

    /**
     * Respuesta de error
     */
    public static function error(string $message, int $status = 400, $data = null): JsonResponse
    {
        $response = [
            'success' => false,
            'error' => $message
        ];

        if ($data) {
            $response['data'] = $data;
        }

        return new JsonResponse($response, $status, [
            'Access-Control-Allow-Origin' => '*',
            'Access-Control-Allow-Methods' => 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers' => 'Content-Type, Authorization'
        ]);
    }

    /**
     * Respuesta paginada
     */
    public static function paginated(array $items, int $total, int $page = 1, int $perPage = 10): JsonResponse
    {
        return self::success([
            'items' => $items,
            'pagination' => [
                'total' => $total,
                'page' => $page,
                'per_page' => $perPage,
                'pages' => ceil($total / $perPage)
            ]
        ]);
    }
}
