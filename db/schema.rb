# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20171114232131) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "api_keys", force: :cascade do |t|
    t.string   "key",        null: false
    t.integer  "user_id"
    t.string   "name",       null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["key"], name: "index_api_keys_on_key", unique: true, using: :btree
    t.index ["user_id"], name: "index_api_keys_on_user_id", using: :btree
  end

  create_table "event_actions", force: :cascade do |t|
    t.integer  "event_receiver_id"
    t.string   "email_address"
    t.string   "webhook_url"
    t.text     "webhook_body"
    t.datetime "created_at",                   null: false
    t.datetime "updated_at",                   null: false
    t.integer  "job_type_id"
    t.string   "type",              limit: 20, null: false
    t.text     "email_body"
    t.index ["event_receiver_id"], name: "index_event_actions_on_event_receiver_id", using: :btree
    t.index ["job_type_id"], name: "index_event_actions_on_job_type_id", using: :btree
  end

  create_table "event_dispatchers", force: :cascade do |t|
    t.boolean  "triggered",         default: false, null: false
    t.integer  "event_receiver_id",                 null: false
    t.datetime "created_at",                        null: false
    t.datetime "updated_at",                        null: false
    t.integer  "job_id",                            null: false
    t.index ["event_receiver_id"], name: "index_event_dispatchers_on_event_receiver_id", using: :btree
    t.index ["job_id"], name: "index_event_dispatchers_on_job_id", using: :btree
  end

  create_table "event_receivers", force: :cascade do |t|
    t.datetime "start_time"
    t.integer  "interval"
    t.integer  "job_type_id"
    t.datetime "created_at",  null: false
    t.datetime "updated_at",  null: false
    t.integer  "user_id",     null: false
    t.string   "type",        null: false
    t.text     "regex"
    t.text     "stream"
    t.integer  "return_code"
    t.index ["job_type_id"], name: "index_event_receivers_on_job_type_id", using: :btree
    t.index ["user_id"], name: "index_event_receivers_on_user_id", using: :btree
  end

  create_table "friendly_id_slugs", force: :cascade do |t|
    t.string   "slug",                      null: false
    t.integer  "sluggable_id",              null: false
    t.string   "sluggable_type", limit: 50
    t.string   "scope"
    t.datetime "created_at"
    t.index ["slug", "sluggable_type", "scope"], name: "index_friendly_id_slugs_on_slug_and_sluggable_type_and_scope", unique: true, using: :btree
    t.index ["slug", "sluggable_type"], name: "index_friendly_id_slugs_on_slug_and_sluggable_type", using: :btree
    t.index ["sluggable_id"], name: "index_friendly_id_slugs_on_sluggable_id", using: :btree
    t.index ["sluggable_type"], name: "index_friendly_id_slugs_on_sluggable_type", using: :btree
  end

  create_table "job_types", force: :cascade do |t|
    t.text     "script"
    t.string   "working_directory"
    t.text     "environment_variables"
    t.integer  "timeout"
    t.string   "name"
    t.integer  "user_id"
    t.datetime "created_at",            null: false
    t.datetime "updated_at",            null: false
    t.index ["user_id"], name: "index_job_types_on_user_id", using: :btree
  end

  create_table "jobs", force: :cascade do |t|
    t.text     "stdout"
    t.text     "stderr"
    t.string   "status"
    t.integer  "return_code"
    t.integer  "job_type_id", null: false
    t.datetime "created_at",  null: false
    t.datetime "updated_at",  null: false
    t.integer  "worker_id",   null: false
    t.index ["job_type_id"], name: "index_jobs_on_job_type_id", using: :btree
    t.index ["worker_id"], name: "index_jobs_on_worker_id", using: :btree
  end

  create_table "users", force: :cascade do |t|
    t.string   "email",                  default: "", null: false
    t.datetime "created_at",                          null: false
    t.datetime "updated_at",                          null: false
    t.string   "encrypted_password",     default: "", null: false
    t.string   "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer  "sign_in_count",          default: 0,  null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.inet     "current_sign_in_ip"
    t.inet     "last_sign_in_ip"
    t.index ["email"], name: "index_users_on_email", unique: true, using: :btree
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true, using: :btree
  end

  create_table "workers", force: :cascade do |t|
    t.integer  "user_id",                          null: false
    t.datetime "last_heartbeat"
    t.datetime "created_at",                       null: false
    t.datetime "updated_at",                       null: false
    t.integer  "cpu_count"
    t.float    "load"
    t.float    "total_memory"
    t.float    "available_memory"
    t.float    "total_disk"
    t.float    "used_disk"
    t.float    "free_disk"
    t.string   "slug"
    t.boolean  "deleted",          default: false, null: false
    t.index ["slug"], name: "index_workers_on_slug", unique: true, using: :btree
    t.index ["user_id"], name: "index_workers_on_user_id", using: :btree
  end

  add_foreign_key "api_keys", "users"
  add_foreign_key "event_actions", "event_receivers"
  add_foreign_key "event_actions", "job_types"
  add_foreign_key "event_dispatchers", "event_receivers"
  add_foreign_key "event_receivers", "job_types"
  add_foreign_key "event_receivers", "users"
  add_foreign_key "job_types", "users"
  add_foreign_key "jobs", "job_types"
  add_foreign_key "jobs", "workers"
  add_foreign_key "workers", "users"
end
