package com.example.bankcustomerapi.controller;

import com.example.bankcustomerapi.model.Customer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/customers")
public class CustomerController {
    private static final Logger logger = LoggerFactory.getLogger(CustomerController.class);
    private Map<String, Customer> customerDb = new HashMap<>();

    @PostMapping
    public ResponseEntity<?> createCustomer(@RequestBody Customer customer) {
        String correlationId = MDC.get("correlationId");
        customer.setId(UUID.randomUUID().toString());
        customerDb.put(customer.getId(), customer);
        logger.info("[{}] Customer created: {}", correlationId, customer.getId());
        return ResponseEntity.ok(customer);
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getCustomer(@PathVariable String id) {
        String correlationId = MDC.get("correlationId");
        if (!customerDb.containsKey(id)) {
            logger.error("[{}][ERR404] Customer not found: {}", correlationId, id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("ERR404: Customer not found");
        }
        logger.info("[{}] Customer fetched: {}", correlationId, id);
        return ResponseEntity.ok(customerDb.get(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateCustomer(@PathVariable String id, @RequestBody Customer customer) {
        String correlationId = MDC.get("correlationId");
        if (!customerDb.containsKey(id)) {
            logger.error("[{}][ERR404] Update failed, customer not found: {}", correlationId, id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("ERR404: Customer not found");
        }
        Customer existing = customerDb.get(id);
        existing.setName(customer.getName());
        existing.setEmail(customer.getEmail());
        logger.info("[{}] Customer updated: {}", correlationId, id);
        return ResponseEntity.ok(existing);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteCustomer(@PathVariable String id) {
        String correlationId = MDC.get("correlationId");
        if (!customerDb.containsKey(id)) {
            logger.error("[{}][ERR404] Delete failed, customer not found: {}", correlationId, id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("ERR404: Customer not found");
        }
        customerDb.remove(id);
        logger.info("[{}] Customer deleted: {}", correlationId, id);
        return ResponseEntity.ok("Deleted");
    }

    @GetMapping("/error")
    public ResponseEntity<?> generateError() {
        String correlationId = MDC.get("correlationId");
        logger.error("[{}][ERR500] Simulated server error occurred", correlationId);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("ERR500: Simulated server error");
    }
}
