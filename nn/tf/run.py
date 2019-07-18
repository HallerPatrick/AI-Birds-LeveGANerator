import tensorflow as tf

from gan import GAN


def main():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        gan = GAN(sess, epoch=100, batch_size=32, z_dim=100, dataset_name="../samples/pig",
                  checkpoint_dir="checkpoints", result_dir="results", log_dir="log")

        gan.build_model()
        gan.train()

        gan.visualize_results(99)


if __name__ == "__main__":
    main()
